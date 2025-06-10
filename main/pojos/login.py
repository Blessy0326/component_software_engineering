# Author: Blessy
# Date: 2025-06-01

# 10. login.html
class LoginData:
    """
    Data class for login form
    Corresponds to: login.html form
    """
    def __init__(self, email='', password='', role='client', captcha=''):
        self.email = email  # String: user's email
        self.password = password  # String: user's password
        self.role = role  # String: either 'client' or 'provider'
        self.captcha = captcha  # String: CAPTCHA input
    
    def __str__(self):
        return f"Login({self.email}, role={self.role})"