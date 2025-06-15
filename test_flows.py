import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import Chatbot
from load_data import load_and_store_data

class TestChatbotPipeline(unittest.TestCase):
    """
    Bộ kiểm thử toàn diện cho các luồng hội thoại chính của Chatbot.
    """

    @classmethod
    def setUpClass(cls):
        """Chạy một lần duy nhất trước tất cả các test để chuẩn bị dữ liệu."""
        print("--- Đang chuẩn bị dữ liệu cho môi trường test ---")
        try:
            load_and_store_data()
            print("--- Dữ liệu đã sẵn sàng ---")
        except Exception as e:
            print(f"Lỗi khi chuẩn bị dữ liệu: {e}")
            sys.exit(1)

    def setUp(self):
        """Chạy trước mỗi bài test để khởi tạo chatbot mới."""
        self.chatbot = Chatbot()

    def test_l1_faq_flow(self):
        """Kiểm thử luồng L1: Trả lời câu hỏi thường gặp (FAQ)."""
        print("\n>>> Bắt đầu kiểm thử: Luồng FAQ (L1)")
        user_input = "Hướng dẫn check-in online?"
        
        print(f"    - User: '{user_input}'")
        response = self.chatbot.get_response(user_input)
        print(f"    - Bot: '{response}'")

        self.assertTrue("check-in online" in response or "mã đặt chỗ" in response or "PNR" in response)


    def test_l2_change_ticket_flow(self):
        """Kiểm thử luồng L2: Đổi vé xe."""
        print("\n>>> Bắt đầu kiểm thử: Luồng Đổi Vé (L2)")
        steps = [
            ("đổi vé", "Chắc chắn rồi. Vui lòng cho tôi biết mã vé của bạn."),
            ("VXR123456", "Cảm ơn bạn. Bạn muốn đổi vé sang mấy giờ?"),
            ("18:00 30-12-2025", "Yêu cầu đổi vé VXR123456 sang 18:00 30-12-2025 đã được thực hiện thành công!")
        ]

        for user_input, expected_response in steps:
            print(f"    - User: '{user_input}'")
            actual_response = self.chatbot.get_response(user_input)
            print(f"    - Bot: '{actual_response}'")
            self.assertEqual(actual_response, expected_response)
        
        self.assertIsNone(self.chatbot.state.current_flow)
        print(">>> Kết thúc kiểm thử: Luồng Đổi Vé (L2) - THÀNH CÔNG")

    def test_l3_booking_flow(self):
        """Kiểm thử luồng L3: Đặt vé xe với đầy đủ thông tin hành khách."""
        print("\n>>> Bắt đầu kiểm thử: Luồng Đặt Vé (L3) - Mở rộng")
        
        steps = [
            ("đặt vé", "Rất sẵn lòng! Bạn muốn đặt vé xe khách hay máy bay?"),
            ("xe khách", "Tuyệt vời! Bạn muốn đi từ đâu?"),
            ("Hà Nội", "Bạn muốn đến đâu?"),
            ("Đà Nẵng", "Bạn muốn đi vào ngày nào?"),
            ("25-12-2025", "Tôi đã tìm thấy các chuyến đi sau cho bạn:\n- Chuyến VRX001: khởi hành lúc 25-12-2025 07:00, giá 220000\n- Chuyến VRX002: khởi hành lúc 25-12-2025 09:30, giá 250000\n- Chuyến VRX003: khởi hành lúc 25-12-2025 13:00, giá 240000\nVui lòng chọn mã chuyến đi bạn muốn đặt (ví dụ: VXR01)."),
            ("VRX001", "Cảm ơn bạn. Vui lòng cho tôi biết tên đầy đủ của hành khách."),
            ("nguyễn cao chánh", "Vui lòng cung cấp số điện thoại liên lạc của bạn."),
            ("0379009341", "Đặt vé thành công! Mã đặt chỗ của bạn là")
        ]
        
        for i, (user_input, expected_response) in enumerate(steps):
            print(f"    - User: '{user_input}'")
            actual_response = self.chatbot.get_response(user_input)
            print(f"    - Bot: '{actual_response}'")
            
            if "Mã đặt chỗ của bạn là" in expected_response:
                self.assertIn(expected_response, actual_response)
            else:
                self.assertEqual(actual_response, expected_response)
        
        self.assertIsNone(self.chatbot.state.current_flow)
        print(">>> Kết thúc kiểm thử: Luồng Đặt Vé (L3) - Mở rộng - THÀNH CÔNG")

if __name__ == '__main__':
    unittest.main(verbosity=2)