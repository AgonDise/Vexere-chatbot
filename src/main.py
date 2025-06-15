import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from .state import ConversationState
from .services import (
    change_ticket_time_api, 
    search_trips_api, 
    create_booking_api,
    process_ticket_image
)

load_dotenv()

class Chatbot:
    def __init__(self):
        self.rag_chain = self._initialize_rag_chain()
        self.state = ConversationState()
        print("Chatbot đã sẵn sàng!")

    def _initialize_rag_chain(self):
        """Khởi tạo chuỗi RAG để trả lời các câu hỏi FAQ."""
        print("Đang khởi tạo chuỗi RAG-FAQ...")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
        embeddings = HuggingFaceEmbeddings(model_name="hiieu/halong_embedding")
        vectordb = Chroma(persist_directory="vectordb", embedding_function=embeddings)
        retriever = vectordb.as_retriever(search_kwargs={"k": 2})
        
        prompt_template = "Dựa vào thông tin sau đây để trả lời câu hỏi: {context}\n\nCâu hỏi: {question}\n\nTrả lời:"
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=retriever,
            return_source_documents=False, chain_type_kwargs={"prompt": PROMPT}
        )
        print("Khởi tạo chuỗi RAG-FAQ hoàn tất.")
        return qa_chain


    def get_response(self, user_input: str) -> str:
        """Xử lý đầu vào của người dùng và trả về phản hồi."""
        active_flow = self.state.current_flow

        if active_flow == 'book_ticket':
            return self._handle_booking_flow(user_input)
        elif active_flow == 'change_ticket_time':
            return self._handle_change_ticket_flow(user_input)
        
        else:
            if any(keyword in user_input.lower() for keyword in ["đặt vé", "mua vé"]):
                self.state.start_flow('book_ticket')
                return "Rất sẵn lòng! Bạn muốn đặt vé xe khách hay máy bay?"
            elif any(keyword in user_input.lower() for keyword in ["đổi giờ", "đổi vé"]):
                self.state.start_flow('change_ticket_time')
                return "Chắc chắn rồi. Vui lòng cho tôi biết mã vé của bạn."
            elif any(keyword in user_input.lower() for keyword in ["gửi ảnh", "ảnh vé"]):
                return self._handle_image_submission()
            else:
                result = self.rag_chain.invoke({"query": user_input})
                return result['result']

    def _handle_image_submission(self):
        """Mô phỏng luồng xử lý khi người dùng gửi ảnh."""
        mock_image_data = b"some_image_bytes"
        result = process_ticket_image(mock_image_data)

        if result.get("success"):
            self.state.start_flow('change_ticket_time')
            self.state.slots['booking_code'] = result['booking_code']
            self.state.transition_to('AWAITING_NEW_TIME') 
            return f"Tôi thấy mã vé của bạn là {result['booking_code']}. Bạn muốn đổi vé sang mấy giờ?"
        else:
            return "Rất tiếc, tôi không thể đọc được thông tin từ ảnh của bạn. Vui lòng nhập mã vé thủ công."

    def _handle_change_ticket_flow(self, user_input: str) -> str:
        """Xử lý luồng đổi vé L2."""
        if self.state.current_state == 'AWAITING_BOOKING_CODE':
            self.state.slots['booking_code'] = user_input
            self.state.transition_to('AWAITING_NEW_TIME')
            return "Cảm ơn bạn. Bạn muốn đổi vé sang mấy giờ?"
        
        elif self.state.current_state == 'AWAITING_NEW_TIME':
            self.state.slots['new_time'] = user_input
            result = change_ticket_time_api(
                booking_code=self.state.slots['booking_code'],
                new_time=self.state.slots['new_time']
            )
            self.state.reset()
            return result['message']

    def _handle_booking_flow(self, user_input: str) -> str:
        """Xử lý luồng đặt vé L3."""
        if self.state.current_state == 'AWAITING_TRIP_TYPE':
            self.state.slots['trip_type'] = user_input
            self.state.transition_to('AWAITING_ORIGIN')
            return "Tuyệt vời! Bạn muốn đi từ đâu?"

        elif self.state.current_state == 'AWAITING_ORIGIN':
            self.state.slots['origin'] = user_input
            self.state.transition_to('AWAITING_DESTINATION')
            return "Bạn muốn đến đâu?"

        elif self.state.current_state == 'AWAITING_DESTINATION':
            self.state.slots['destination'] = user_input
            self.state.transition_to('AWAITING_DATE')
            return "Bạn muốn đi vào ngày nào?"

        elif self.state.current_state == 'AWAITING_DATE':
            self.state.slots['date'] = user_input
            result = search_trips_api(
                origin=self.state.slots['origin'],
                destination=self.state.slots['destination'],
                date=self.state.slots['date']
            )
            if result.get("success") and result.get("trips"):
                self.state.slots['available_trips'] = result['trips']
                response = "Tôi đã tìm thấy các chuyến đi sau cho bạn:\n"
                for trip in result['trips']:
                    response += f"- Chuyến {trip['trip_id']}: khởi hành lúc {trip['departure_time']}, giá {trip['price']}\n"
                response += "Vui lòng chọn mã chuyến đi bạn muốn đặt (ví dụ: VXR01)."
                self.state.transition_to('AWAITING_TRIP_SELECTION')
                return response
            else:
                self.state.reset()
                return "Rất tiếc, tôi không tìm thấy chuyến đi nào phù hợp. Bạn có muốn thử tìm kiếm lại không?"

        elif self.state.current_state == 'AWAITING_TRIP_SELECTION':
            selected_trip_id = user_input.upper()
            available_trips = self.state.slots.get('available_trips',)
            if any(trip['trip_id'] == selected_trip_id for trip in available_trips):
                self.state.slots['selected_trip_id'] = selected_trip_id
                self.state.transition_to('AWAITING_PASSENGER_NAME')
                return "Cảm ơn bạn. Vui lòng cho tôi biết tên đầy đủ của hành khách."
            else:
                return "Mã chuyến đi không hợp lệ. Vui lòng chọn lại."

        elif self.state.current_state == 'AWAITING_PASSENGER_NAME':
            self.state.slots['passenger_name'] = user_input
            self.state.transition_to('AWAITING_CONTACT_NUMBER')
            return "Vui lòng cung cấp số điện thoại liên lạc của bạn."

        elif self.state.current_state == 'AWAITING_CONTACT_NUMBER':
            self.state.slots['contact_number'] = user_input
            result = create_booking_api(
                trip_id=self.state.slots['selected_trip_id'],
                passenger_name=self.state.slots['passenger_name'],
                contact_number=self.state.slots['contact_number']
            )
            self.state.reset()
            return result['message']
        
        return "Xin lỗi, tôi chưa hiểu ý bạn. Chúng ta đang trong quá trình đặt vé."

def interactive_chat():
    if not os.getenv("GOOGLE_API_KEY"):
        print("\nLỖI: Vui lòng thiết lập GOOGLE_API_KEY trong file.env của bạn.")
        return
        
    chatbot = Chatbot()
    print("Chào mừng bạn đến với Chatbot của Vexere!")
    print("Gõ 'thoát' để kết thúc.")

    while True:
        user_input = input("\nBạn: ")
        if user_input.lower() == 'thoát':
            print("Cảm ơn bạn đã sử dụng. Tạm biệt!")
            break
        
        response = chatbot.get_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    interactive_chat()
