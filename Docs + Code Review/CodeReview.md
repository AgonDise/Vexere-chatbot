Code Review Self-Check
1. Code Style Conventions
Naming Conventions:

Tên biến và tên hàm sử dụng snake_case (ví dụ: booking_code, handle_user_input). [cite: src/main.py]

Tên lớp (class) sử dụng PascalCase (ví dụ: Chatbot, ConversationState). [cite: src/main.py, src/state.py]

Hằng số được viết hoa toàn bộ (ví dụ: AWAITING_BOOKING_CODE). [cite: src/state.py]

Cấu trúc tệp:

Mã nguồn được tổ chức thành các mô-đun riêng biệt theo chức năng:

main.py: Chứa logic chính của chatbot và điều phối các luồng. [cite: src/main.py]

state.py: Quản lý trạng thái của cuộc hội thoại. [cite: src/state.py]

services.py: Chứa các hàm giao tiếp với bên ngoài (API, xử lý đa phương tiện) dưới dạng giả lập. [cite: src/services.py]

load_data.py: Xử lý và nạp dữ liệu cho RAG. [cite: load_data.py]

2. Testing & Continuous Integration
Testing:

integration testingcho các luồng hội thoại end-to-end.

Tệp test_flows.py sử dụng thư viện unittest của Python để định nghĩa các kịch bản kiểm thử. [cite: test_flows.py]

Các kịch bản này bao gồm:

Kiểm tra luồng trả lời câu hỏi FAQ (L1). [cite: test_flows.py]

Kiểm tra luồng thay đổi giờ vé (L2) từ đầu đến cuối. [cite: test_flows.py]

Kiểm tra luồng đặt vé (L3), đảm bảo bot thu thập đủ thông tin. [cite: test_flows.py]

CI:

Sử dụng GitHub Actions để thiết lập một pipeline CI đơn giản, được định nghĩa trong tệp .github/workflows/ci.yml. [cite: agondise/vexere-chatbot/Vexere-chatbot-a960ca616adf261a5214ee6c2c1b6b58d914091a/.github/workflows/ci.yml]

Pipeline này được kích hoạt tự động mỗi khi có một push hoặc pull_request được tạo vào nhánh main. [cite: agondise/vexere-chatbot/Vexere-chatbot-a960ca616adf261a5214ee6c2c1b6b58d914091a/.github/workflows/ci.yml]

Các bước trong pipeline bao gồm: cài đặt môi trường Python, cài đặt các thư viện từ requirements.txt, và chạy bộ kiểm thử. [cite: agondise/vexere-chatbot/Vexere-chatbot-a960ca616adf261a5214ee6c2c1b6b58d914091a/.github/workflows/ci.yml]

3. Điểm Còn Hạn Chế & Hướng Mở Rộng
Đây là một PoC nên có một số hạn chế cần được cải thiện để triển khai trong môi trường production.

Điểm còn hạn chế:

Quản lý trạng thái: Trạng thái hội thoại hiện đang được lưu trong bộ nhớ (in-memory). [cite: src/state.py] Điều này không phù hợp cho môi trường production với nhiều người dùng đồng thời vì trạng thái sẽ bị mất khi khởi động lại ứng dụng.

Cơ sở dữ liệu Vector: Sử dụng ChromaDB chạy local rất tiện cho PoC nhưng không có khả năng mở rộng về dung lượng và hiệu năng truy vấn. [cite: src/main.py]

Tích hợp API: Các hàm gọi API trong services.py hiện chỉ là giả lập (mock). [cite: src/services.py]

Xử lý đa phương tiện: Các hàm xử lý ảnh và giọng nói chỉ là các placeholder và chưa có logic thực tế. [cite: src/services.py]

Nhận dạng ý định: Việc xác định ý định của người dùng còn đơn giản, chủ yếu dựa vào từ khóa. [cite: src/main.py]

Hướng mở rộng và cải tiến:

Quản lý trạng thái: Chuyển sang sử dụng một giải pháp lưu trữ ngoài như Redis hoặc một cơ sở dữ liệu để quản lý phiên làm việc của người dùng.

Cơ sở dữ liệu Vector: Nâng cấp lên một dịch vụ vector database chuyên dụng và có khả năng mở rộng như Pinecone, Weaviate hoặc Vertex AI Vector Search.

Tích hợp thực tế: Xây dựng các client để gọi đến API backend thực sự của Vexere, với cơ chế xử lý lỗi và retry.

Hoàn thiện đa phương tiện: Tích hợp các mô hình/dịch vụ thực tế:

Voice-to-Text: Sử dụng OpenAI Whisper hoặc Google Speech-to-Text API.

Image Processing: Sử dụng Google Vision API để đọc thông tin từ ảnh chụp vé của người dùng.

Nâng cao NLU: Tích hợp một module NLU (Natural Language Understanding) để nhận dạng ý định và trích xuất thực thể (entities) một cách chính xác hơn, có thể sử dụng chính khả năng function calling của các LLM hiện đại.

Logging và Monitoring: Xây dựng hệ thống logging chi tiết để theo dõi các cuộc hội thoại và dễ dàng gỡ lỗi khi có sự cố.
