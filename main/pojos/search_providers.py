# Author: Blessy
# Date: 2025-06-01

# 22. search_providers.html
class ProviderSearchData:
    """
    Data class for provider search form
    Corresponds to: search_providers.html form
    """
    def __init__(self, name='', specialty='', location='', rating=''):
        self.name = name  # String: provider name to search for
        self.specialty = specialty  # String: medical specialty filter
        self.location = location  # String: location filter
        self.rating = rating  # String: minimum rating filter
    
    def __str__(self):
        return f"ProviderSearch(name={self.name}, specialty={self.specialty}, location={self.location})"