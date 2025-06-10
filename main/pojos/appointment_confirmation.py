# Author: Blessy
# Date: 2025-06-01


# 2. appointment_confirmation.html (no form - display only)
class AppointmentConfirmationData:
    """
    Data class for appointment confirmation display
    Corresponds to: appointment_confirmation.html
    """
    def __init__(self, provider_name='', appointment_date='', appointment_time=''):
        self.provider_name = provider_name  # String: provider name
        self.appointment_date = appointment_date  # String: appointment date
        self.appointment_time = appointment_time  # String: appointment time
    
    def __str__(self):
        return f"Confirmation({self.provider_name}, {self.appointment_date} at {self.appointment_time})"