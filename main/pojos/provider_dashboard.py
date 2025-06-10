# Author: Blessy
# Date: 2025-06-01

# 17. provider_dashboard.html
class ProviderDashboardData:
    """
    Data class for provider dashboard appointment actions
    Corresponds to: provider_dashboard.html form
    """
    def __init__(self, appointment_id='', client_name='', action=''):
        self.appointment_id = appointment_id  # String: unique identifier for appointment
        self.client_name = client_name  # String: name of the client
        self.action = action  # String: 'accept', 'reschedule', or 'complete'
    
    def __str__(self):
        return f"ProviderDashboard({self.client_name}, action={self.action})"