# Author: Blessy
# Date: 2025-06-01

# 19. provider_sync_calendar.html
class CalendarSyncData:
    """
    Data class for calendar synchronization
    Corresponds to: provider_sync_calendar.html form
    """
    def __init__(self, calendar_link=''):
        self.calendar_link = calendar_link  # String: Google Calendar link or URL
    
    def __str__(self):
        return f"CalendarSync(link={self.calendar_link})"