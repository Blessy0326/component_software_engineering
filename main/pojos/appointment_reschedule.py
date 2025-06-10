# Author: Blessy
# Date: 2025-06-01


# 3. appointment_reschedule.html
class AppointmentRescheduleData:
    """
    Data class for appointment rescheduling form
    Corresponds to: appointment_reschedule.html form
    """
    def __init__(self, date='', time=''):
        self.date = date  # String: new appointment date (YYYY-MM-DD format)
        self.time = time  # String: new appointment time (HH:MM format)
    
    def __str__(self):
        return f"Reschedule(new date: {self.date}, new time: {self.time})"