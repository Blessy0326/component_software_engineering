# Author: Blessy
# Date: 2025-06-01

# 9. index.html (home page - navigation only)
class IndexData:
    """
    Data class for home page navigation
    Corresponds to: index.html
    """
    def __init__(self, selected_action=''):
        self.selected_action = selected_action  # String: 'search', 'register', or 'login'
    
    def __str__(self):
        return f"HomePage(action={self.selected_action})"