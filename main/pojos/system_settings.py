# Author: Blessy
# Date: 2025-06-01

# 23. system_settings.html
class SystemSettingsData:
    """
    Data class for system configuration settings
    Corresponds to: system_settings.html form
    """
    def __init__(self, appointment_duration='', buffer_time=''):
        self.appointment_duration = appointment_duration  # String: duration in minutes
        self.buffer_time = buffer_time  # String: buffer time in minutes
    
    def __str__(self):
        return f"SystemSettings(duration={self.appointment_duration}, buffer={self.buffer_time})"