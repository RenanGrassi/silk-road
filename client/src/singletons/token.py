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

    @classmethod
    def get_token_kwargs(cls):
        """
        Returns a dictionary with the token for use in service calls.
        :return: A dictionary containing the token.
        """
        return {"token": cls.get_token()} if cls.get_token() else {}
