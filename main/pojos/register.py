# Author: Blessy
# Date: 2025-06-01

# 20. register.html
class RegistrationData:
    """
    Data class for user registration form
    Corresponds to: register.html form
    """
    def __init__(self, terms=False, name='', email='', password='', role='client',
                 captcha='', specialty=None, experience=None, location=None, availability=None):
        self.terms = terms  # Boolean: accepted terms
        self.name = name  # String: user's name
        self.email = email  # String: user's email
        self.password = password  # String: user's password
        self.role = role  # String: either 'client' or 'provider'
        self.captcha = captcha  # String: CAPTCHA input
        # Provider-specific fields (optional)
        self.specialty = specialty  # String: area of specialization
        self.experience = experience  # String or int: experience in years
        self.location = location  # String: provider's location
        self.availability = availability  # String: availability details
    
    def __str__(self):
        return f"{self.role.capitalize()}({self.name}, {self.email})"