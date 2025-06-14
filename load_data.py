# load_data.py

import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

# Tải các biến môi trường từ file.env (nếu có)
load_dotenv()

# --- Cấu hình ---
# Sử dụng mô hình embedding miễn phí từ Hugging Face
embeddings = HuggingFaceEmbeddings(model_name="hiieu/halong_embedding")

# Đường dẫn đến file CSV và thư mục lưu trữ VectorDB
FAQ_CSV_PATH = "data/faq_vexere.csv"
VECTOR_DB_PATH = "vectordb"

def load_and_store_data():
    """
    Hàm để tải dữ liệu từ CSV, tạo embeddings và lưu vào ChromaDB.
    """
    # 1. Tải dữ liệu từ file CSV
    if not os.path.exists(FAQ_CSV_PATH):
        print(f"Lỗi: Không tìm thấy file {FAQ_CSV_PATH}")
        return
        
    df = pd.read_csv(FAQ_CSV_PATH)
    # Kết hợp câu hỏi và câu trả lời thành một cột 'text' để embedding
    df['text'] = "Câu hỏi: " + df['question'] + "\nCâu trả lời: " + df['answer']
    
    # Sử dụng DataFrameLoader của LangChain
    loader = DataFrameLoader(df, page_content_column="text")
    documents = loader.load()
    
    print(f"Đã tải {len(documents)} tài liệu từ file CSV.")

    # 2. Phân chia tài liệu (tùy chọn, nhưng tốt cho các văn bản dài)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # 3. Tạo và lưu trữ VectorDB
    print("Đang tạo và lưu trữ vector database...")
    vectordb = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    
    print(f"Đã lưu trữ thành công vào {VECTOR_DB_PATH}")

if __name__ == "__main__":
    load_and_store_data()