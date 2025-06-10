# Author: Blessy
# Date: 2025-06-01

# 13. manage_reviews.html
class ReviewManagementData:
    """
    Data class for replying to client reviews
    Corresponds to: manage_reviews.html form
    """
    def __init__(self, review_id='', client_name='', reply_text=''):
        self.review_id = review_id  # String: identifier for the review being replied to
        self.client_name = client_name  # String: name of client who left review
        self.reply_text = reply_text  # String: reply text from textarea
    
    def __str__(self):
        return f"ReviewMgmt(client={self.client_name}, reply='{self.reply_text[:50]}...')"