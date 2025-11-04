from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model


class EmailVerificationTokenGenerator:
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """

    def make_token(user):
        """
        Return a token that can be used once to do a password reset
        for the given user.

        Args:
            user (Model): the user
            expiry (datetime | int): optional forced expiry date
            kwargs: extra payload for the token

        Returns:
             (tuple): tuple containing:
                token (str): the token
                expiry (datetime): the expiry datetime
        """
        payload = {'email': user.email}

        return jwt.encode(payload, 'secret', algorithm='HS256')

    def check_token(token):
        """
        Check that a password reset token is correct.
        Args:
            token (str): the token from the url
            kwargs: the extra required payload

        Returns:
            (tuple): tuple containing:
                valid (bool): True if the token is valid
                user (Model): the user model if the token is valid
        """

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            email = payload['email']

        except (ValueError, get_user_model().DoesNotExist, jwt.DecodeError, jwt.ExpiredSignatureError):
            return False

        return email

