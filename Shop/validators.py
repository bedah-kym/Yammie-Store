from django.core.exceptions import ValidationError


class locationvalidation:
    def __init__(self,location,min_length=8):
        """
        this function checks if what you input is a real location (using data loaded from a separate library
        im working on ,for now it just checks if the location is a word with a min length
        """

        self.min_length = min_length
        self.location = location

        def validate(self):
            if len(self.location) < self.min_length :
                raise ValidationError(("This password must contain at least %(min_length)d characters."),code='password_too_short',params={'min_length': self.min_length})
