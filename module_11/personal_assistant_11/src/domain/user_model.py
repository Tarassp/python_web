class User:
    def __init__(self, name: str, email: str, p_hash: str, token_cookie: str | None = None):
        self.username = name
        self.email = email
        self.p_hash = p_hash
        self.token_cookie = token_cookie

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return other.email == self.email

    def __hash__(self):
        return hash(self.email)

    def __repr__(self):
        return f"User({self.username}, {self.email})"
