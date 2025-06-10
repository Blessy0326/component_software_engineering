# Author: Blessy
# Date: 2025-06-01

# 4. book_appointment.html
class AppointmentBookingData:
    """
    Data class for appointment booking form
    Corresponds to: book_appointment.html form
    """
    def __init__(self, service='', date='', time=''):
        self.service = service  # String: type of service requested
        self.date = date  # String: appointment date (YYYY-MM-DD format)
        self.time = time  # String: appointment time (HH:MM format)
    
    def __str__(self):
        return f"Appointment({self.service}, {self.date} at {self.time})"