# Author: Blessy
# Date: 2025-06-01

# 7. edit_provider_profile.html
class ProviderProfileData:
    """
    Data class for provider profile editing form
    Corresponds to: edit_provider_profile.html form
    """
    def __init__(self, name='', specialty='', experience='', location='', availability=''):
        self.name = name  # String: provider's name
        self.specialty = specialty  # String: area of medical specialization
        self.experience = experience  # String: years or description of experience
        self.location = location  # String: provider's practice location
        self.availability = availability  # String: available days/hours
    
    def __str__(self):
        return f"ProviderProfile({self.name}, {self.specialty}, {self.location})"