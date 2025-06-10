# Author: Blessy
# Date: 2025-06-01

# 15. monitor_bookings.html (display only - no forms)
class BookingMonitorData:
    """
    Data class for booking monitoring display
    Corresponds to: monitor_bookings.html
    """
    def __init__(self, client_name='', provider_name='', booking_date='', booking_time=''):
        self.client_name = client_name  # String: client name
        self.provider_name = provider_name  # String: provider name
        self.booking_date = booking_date  # String: booking date
        self.booking_time = booking_time  # String: booking time
    
    def __str__(self):
        return f"BookingMonitor({self.client_name} -> {self.provider_name}, {self.booking_date})"