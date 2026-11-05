from pwdlib import PasswordHash


def generate_pwd_hash(password: str) -> str:
    hasher = PasswordHash.recommended()
    return hasher.hash(password)    # XXX Does this automatically set a salt? 