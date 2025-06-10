# Author: Blessy
# Date: 2025-06-01

# 18. provider_profile.html (display only - no forms)
class ProviderProfileDisplayData:
    """
    Data class for provider profile display
    Corresponds to: provider_profile.html
    """
    def __init__(self, provider_name='', specialty='', working_hours='', rating=''):
        self.provider_name = provider_name  # String: provider name
        self.specialty = specialty  # String: medical specialty
        self.working_hours = working_hours  # String: working hours
        self.rating = rating  # String: provider rating
    
    def __str__(self):
        return f"ProviderDisplay({self.provider_name}, {self.specialty}, {self.rating})"