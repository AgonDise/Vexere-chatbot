Chắc chắn rồi. Dưới đây là nội dung hoàn chỉnh cho file `README.md` dựa trên cấu trúc đã thảo luận và mã nguồn bạn đã cung cấp. Bạn có thể sao chép và dán trực tiếp vào file `README.md` trong dự án của mình.

---

# **Vexere AI Chatbot - POC**

Dự án này là một Proof-of-Concept (POC) cho hệ thống AI Chatbot của Vexere, được thực hiện trong khuôn khổ bài test vị trí AI Engineer. Chatbot có khả năng trả lời câu hỏi, xử lý yêu cầu sau bán hàng và hỗ trợ đặt vé, dựa trên kiến trúc có khả năng mở rộng.

## **Tính năng chính**

* **L1 - FAQ:** Trả lời các câu hỏi thường gặp của người dùng (lấy từ file `faq_vexere.csv`) sử dụng kỹ thuật RAG (Retrieval-Augmented Generation).
* **L2 - After-Service:** Xử lý luồng nghiệp vụ **Đổi giờ vé**, được định nghĩa trong `_handle_change_ticket_flow`.
* **L3 - Đặt vé (Bonus):** Hỗ trợ người dùng thực hiện luồng đặt vé xe khách từ đầu đến cuối.
* **Kiến trúc mở rộng:** Hệ thống được thiết kế để sẵn sàng tích hợp các tính năng xử lý **âm thanh (voice)** và **hình ảnh (image)** thông qua các hàm giữ chỗ trong `src/services.py`.
* **Kiểm thử tự động:** Tích hợp bộ test case toàn diện cho các luồng hội thoại trong `test_flows.py` và quy trình CI với GitHub Actions.

## **Công nghệ sử dụng**

* **Ngôn ngữ:** Python
* **Core AI/LLM:** `langchain`, `google-generativeai`
* **Vector Database:** `chromadb`
* **Embeddings Model:** `sentence-transformers`
* **Testing:** `pytest`
* **CI/CD:** GitHub Actions

## **Cài đặt và Chạy dự án**

### **1. Yêu cầu**
* Python 3.9+
* Git

### **2. Các bước cài đặt**
```bash
# 1. Clone repository
git clone <your-repo-url>
cd <your-repo-directory>

# 2. Tạo môi trường ảo (khuyến khích)
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 4. Cấu hình API Key
# Tạo file .env ở thư mục gốc và thêm Google API Key của bạn.
# File .env được liệt kê trong .gitignore để bảo mật.
echo "GOOGLE_API_KEY='your-google-api-key'" > .env

# 5. Chuẩn bị dữ liệu cho RAG
# Lệnh này sẽ tải dữ liệu, tạo embeddings và lưu vào ChromaDB.
python load_data.py
```

### **3. Chạy ứng dụng**
Để bắt đầu một phiên chat trong giao diện dòng lệnh:
```bash
python -m src.main
```

### **4. Chạy kiểm thử**
Để chạy tất cả các test case và đảm bảo các luồng hoạt động chính xác:
```bash
pytest
```
---
