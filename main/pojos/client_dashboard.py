# Author: Blessy
# Date: 2025-06-01

# 5. client_dashboard.html (navigation only - no form)
class ClientDashboardData:
    """
    Data class for client dashboard navigation
    Corresponds to: client_dashboard.html
    """
    def __init__(self, selected_action=''):
        self.selected_action = selected_action  # String: 'book', 'manage', or 'logout'
    
    def __str__(self):
        return f"ClientDashboard(action={self.selected_action})"