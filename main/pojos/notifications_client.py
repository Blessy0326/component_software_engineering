# Author: Blessy
# Date: 2025-06-01

# 16. notifications_client.html (display only - no forms)
class ClientNotificationData:
    """
    Data class for client notifications display
    Corresponds to: notifications_client.html
    """
    def __init__(self, notification_type='', message='', timestamp=''):
        self.notification_type = notification_type  # String: type of notification
        self.message = message  # String: notification message
        self.timestamp = timestamp  # String: when notification was created
    
    def __str__(self):
        return f"Notification({self.notification_type}: {self.message[:50]}...)"