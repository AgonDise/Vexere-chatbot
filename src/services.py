import random

# --- Dịch vụ L2: After-Service ---
def change_ticket_time_api(booking_code: str, new_time: str) -> dict:
    """Mô phỏng việc gọi đến API backend của Vexere để đổi giờ vé."""
    print(f" [API] Đang gọi API đổi vé với mã: {booking_code}, giờ mới: {new_time}")
    if "123" in booking_code:
        return {"success": True, "message": f"Yêu cầu đổi vé {booking_code} sang {new_time} đã được thực hiện thành công!"}
    else:
        return {"success": False, "message": f"Rất tiếc, không thể đổi vé cho mã {booking_code}. Vui lòng kiểm tra lại mã vé."}

# --- Dịch vụ L3: Booking ---
def search_trips_api(origin: str, destination: str, date: str) -> dict:
    """Mô phỏng việc gọi API tìm kiếm các chuyến đi có sẵn."""
    print(f" [API] Đang gọi API tìm chuyến đi: từ {origin} đến {destination} vào ngày {date}")
    return {
        "success": True,
        "trips":[
            {
                "trip_id": "VRX001",
                "bus_company": "Xe Hoàng Long",
                "departure_time": f"{date} 07:00",
                "arrival_time": f"{date} 13:00",
                "price": 220000,
                "seats_available": 8
            },
            {
                "trip_id": "VRX002",
                "bus_company": "Xe Mai Linh",
                "departure_time": f"{date} 09:30",
                "arrival_time": f"{date} 15:00",
                "price": 250000,
                "seats_available": 12
            },
            {
                "trip_id": "VRX003",
                "bus_company": "Xe Phương Trang",
                "departure_time": f"{date} 13:00",
                "arrival_time": f"{date} 18:30",
                "price": 240000,
                "seats_available": 5
            }
        ]
    }

def create_booking_api(trip_id: str, passenger_name: str, contact_number: str) -> dict:
    """Mô phỏng việc gọi API để tạo một đặt chỗ mới."""
    print(f" [API] Đang gọi API tạo đặt chỗ cho chuyến {trip_id} với khách hàng {passenger_name}")
    booking_code = f"VX{random.randint(100000, 999999)}"
    return {
        "success": True,
        "booking_code": booking_code,
        "message": f"Đặt vé thành công! Mã đặt chỗ của bạn là {booking_code}. Cảm ơn bạn đã sử dụng dịch vụ của Vexere."
    }

# --- MỚI: Dịch vụ Đa phương tiện (Placeholder) ---

def process_ticket_image(image_data: bytes) -> dict:
    """
    PLACEHOLDER: Mô phỏng dịch vụ xử lý hình ảnh vé xe.
    Trong thực tế, dịch vụ này sẽ dùng OCR/IDP (ví dụ: LayoutLMv3) để trích xuất thông tin.
    """
    print(" Dịch vụ xử lý ảnh đang phân tích...")
    # Giả lập kết quả trích xuất thành công
    return {
        "success": True,
        "booking_code": "VX_IMG_123",
        "passenger_name": "Nguyen Van An (từ ảnh)"
    }

def speech_to_text(audio_data: bytes) -> str:
    """
    PLACEHOLDER: Mô phỏng dịch vụ chuyển giọng nói thành văn bản (STT/ASR).
    """
    print(" Dịch vụ STT đang phiên âm...")
    # Giả lập kết quả phiên âm
    return "tôi muốn đặt vé đi đà lạt"

def text_to_speech(text: str) -> bytes:
    """
    PLACEHOLDER: Mô phỏng dịch vụ chuyển văn bản thành giọng nói (TTS).
    """
    print(f" Dịch vụ TTS đang tổng hợp âm thanh cho: '{text}'")
    # Trả về dữ liệu âm thanh giả lập
    return b"mock_audio_data"