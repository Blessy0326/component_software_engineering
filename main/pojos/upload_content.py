# Author: Blessy
# Date: 2025-06-01

# 24. upload_content.html
class ContentUploadData:
    """
    Data class for content upload form
    Corresponds to: upload_content.html form
    """
    def __init__(self, title='', content=''):
        self.title = title  # String: title of the content
        self.content = content  # String: content text from textarea (prescription/FAQ/guides)
    
    def __str__(self):
        return f"ContentUpload(title='{self.title}', content='{self.content[:50]}...')"