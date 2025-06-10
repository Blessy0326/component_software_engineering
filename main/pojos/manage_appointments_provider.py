# Author: Blessy
# Date: 2025-06-01

# 11. manage_appointments_provider.html
class ProviderAppointmentManagementData:
    """
    Data class for provider appointment management actions
    Corresponds to: manage_appointments_provider.html form
    """
    def __init__(self, appointment_id='', client_name='', action=''):
        self.appointment_id = appointment_id  # String: unique identifier for appointment
        self.client_name = client_name  # String: name of the client
        self.action = action  # String: 'accept', 'reject', or 'complete'
    
    def __str__(self):
        return f"ProviderAppointmentMgmt({self.client_name}, action={self.action})"