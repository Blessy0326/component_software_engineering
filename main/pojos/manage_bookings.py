# Author: Blessy
# Date: 2025-06-01

# 12. manage_bookings.html
class ClientBookingManagementData:
    """
    Data class for client booking management actions
    Corresponds to: manage_bookings.html form
    """
    def __init__(self, appointment_id='', provider_name='', action=''):
        self.appointment_id = appointment_id  # String: unique identifier for appointment
        self.provider_name = provider_name  # String: name of the provider
        self.action = action  # String: 'cancel' or 'reschedule'
    
    def __str__(self):
        return f"ClientBookingMgmt({self.provider_name}, action={self.action})"