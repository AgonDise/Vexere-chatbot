class ConversationState:
    """
    Quản lý trạng thái của cuộc hội thoại, bao gồm cả luồng và trạng thái hiện tại.
    """
    def __init__(self):
        self.current_flow = None      
        self.current_state = None   
        self.slots = {}  

    def start_flow(self, flow_name: str):
        """MỚI: Bắt đầu một luồng mới và đặt trạng thái ban đầu."""
        print(f"--- Bắt đầu luồng: {flow_name} ---")
        self.current_flow = flow_name
        self.slots = {}
        # Thiết lập trạng thái ban đầu cho từng luồng
        if flow_name == 'book_ticket':
            self.current_state = 'AWAITING_TRIP_TYPE'
        elif flow_name == 'change_ticket_time':
            self.current_state = 'AWAITING_BOOKING_CODE'

    def transition_to(self, new_state: str):
        """MỚI: Chuyển sang một trạng thái mới trong luồng hiện tại."""
        print(f"--- Chuyển trạng thái: từ {self.current_state} -> {new_state} ---")
        self.current_state = new_state

    def reset(self):
        """Reset lại trạng thái sau khi một luồng hoàn thành hoặc bị hủy."""
        print("--- Kết thúc luồng, reset trạng thái. ---")
        self.current_flow = None
        self.current_state = None
        self.slots = {}