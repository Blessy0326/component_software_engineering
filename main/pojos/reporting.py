# Author: Blessy
# Date: 2025-06-01

# 21. reporting.html (display only - no forms)
class ReportingData:
    """
    Data class for analytics and reporting display
    Corresponds to: reporting.html
    """
    def __init__(self, total_bookings=0, no_shows=0, peak_hour=''):
        self.total_bookings = total_bookings  # Integer: total bookings count
        self.no_shows = no_shows  # Integer: no-show count
        self.peak_hour = peak_hour  # String: peak booking hour
    
    def __str__(self):
        return f"Reports(bookings={self.total_bookings}, no_shows={self.no_shows}, peak={self.peak_hour})"