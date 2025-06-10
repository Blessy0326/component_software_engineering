# Author: Blessy
# Date: 2025-06-01


# 1. admin_dashboard.html
class AdminDashboardData:
    """
    Data class for admin dashboard actions
    Corresponds to: admin_dashboard.html
    """
    def __init__(self, provider_name='', approval_action='', appointment_duration='', buffer_time=''):
        self.provider_name = provider_name  # String: provider name for approval
        self.approval_action = approval_action  # String: 'approve' or 'decline'
        self.appointment_duration = appointment_duration  # String: duration in minutes
        self.buffer_time = buffer_time  # String: buffer time in minutes
    
    def __str__(self):
        return f"AdminDashboard(provider={self.provider_name}, action={self.approval_action})"