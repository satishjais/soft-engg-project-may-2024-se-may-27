class AuthorizationTokenRequired(Exception):
    def __init__(self, message="Authorization token is required", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)


class JwtTokenExpired(Exception):
    def __init__(self, message="JWT token has expired, please login again", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)


class InvalidJwtToken(Exception):
    def __init__(self, message="Invalid JWT token, please login again", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)


class NotACreator():
    def __init__(self, message="You're not a creator!"):
        self.message = message
        super().__init__(self.message)


class NotAdmin():
    def __init__(self, message="You're not an admin!"):
        self.message = message
        super().__init__(self.message)