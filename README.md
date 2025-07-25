# Vexere AI Chatbot - POC

## Tính năng chính

* **L1 - FAQ:** Trả lời câu hỏi thường gặp sử dụng kỹ thuật RAG (Retrieval-Augmented Generation). Dữ liệu được lấy từ file `faq_vexere.csv`.
* **L2 - After-Service:** Xử lý task **Đổi giờ vé**.
* **L3 - Đặt vé:** Hỗ trợ người dùng thực hiện luồng đặt vé hoàn chỉnh.
* **Extended for Image and Voices:** Sẵn sàng tích hợp xử lý **Image** và **Voice** qua các hàm chờ trong `src/services.py`. (API giả lập dữ liệu từ Image đã được xử lý qua OCR và voice đã được xử lý thành Text.)
* **Test pipeline CI:** Tích hợp bộ test case cho các luồng hội thoại trong `test_flows.py` và pipeline CI với GitHub Actions.

## Frameworks/Techs Used

* **Ngôn ngữ:** Python
* **Core AI/LLM:** `langchain`, `google-generativeai`, `sentence-transformers`
* **Vector Database:** `chromadb`
* **Testing:** `test_flows.py`

## Cài đặt và Chạy dự án

1.  **Clone repository**
    ```bash
    git clone <https://github.com/AgonDise/Vexere-chatbot>
    cd <your-repo-directory>
    ```

2.  **Tạo môi trường ảo và cài đặt thư viện**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **API Key Configuration**
    Tạo file `.env` ở thư mục gốc và thêm Google API Key của bạn. File này đã được thêm vào `.gitignore` để bảo mật.
    ```bash
    echo "GOOGLE_API_KEY='your-google-api-key'" > .env
    ```

4.  **Load Data cho RAG**
    Chạy script `load_data.py` để xử lý và nạp dữ liệu vào vector store.
    ```bash
    python load_data.py
    ```

## Chạy ứng dụng

* **Chạy Chatbot:**
    ```bash
    python -m src.main
    ```
* **Chạy kiểm thử:**
    ```bash
    python test_flows.py
    ```
