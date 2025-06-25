class GlobalToken:
    """
    A class to manage a global token.
    This is used to store a token that can be accessed globally within the application.
    """

    _token = None

    @classmethod
    def set_token(cls, token):
        cls._token = token

    @classmethod
    def get_token(cls):
        return cls._token

    @classmethod
    def clear_token(cls):
        cls._token = None
