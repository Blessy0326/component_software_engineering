# Author: Blessy
# Date: 2025-06-01

# 6. edit_client_profile.html
class ClientProfileData:
    """
    Data class for client profile editing form
    Corresponds to: edit_client_profile.html form
    """
    def __init__(self, name='', email='', action=''):
        self.name = name  # String: client's name
        self.email = email  # String: client's email address
        self.action = action  # String: 'update' or 'delete'
    
    def __str__(self):
        return f"ClientProfile({self.name}, {self.email}, action={self.action})"