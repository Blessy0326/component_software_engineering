# Author: Blessy
# Date: 2025-06-01

# 8. feedback_rating.html
class FeedbackRatingData:
    """
    Data class for feedback and rating form
    Corresponds to: feedback_rating.html form
    """
    def __init__(self, feedback='', rating='5'):
        self.feedback = feedback  # String: feedback text from textarea
        self.rating = rating  # String: rating from 1-5 select dropdown
    
    def __str__(self):
        return f"Feedback(rating={self.rating}, feedback='{self.feedback[:50]}...')"