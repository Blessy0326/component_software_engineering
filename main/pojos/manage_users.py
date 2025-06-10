# Author: Blessy
# Date: 2025-06-01

# 14. manage_users.html
class UserManagementData:
    """
    Data class for user management actions
    Corresponds to: manage_users.html form
    """
    def __init__(self, user_name='', user_type='provider', action=''):
        self.user_name = user_name  # String: name of user (e.g., "Dr. John Smith")
        self.user_type = user_type  # String: type of user ('provider', 'client', etc.)
        self.action = action  # String: either 'approve' or 'decline'
    
    def __str__(self):
        return f"UserMgmt({self.user_name}, {self.user_type}, {self.action})"