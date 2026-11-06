from pwdlib import PasswordHash


def generate_pwd_hash(password: str) -> str:
    hasher = PasswordHash.recommended()
    return hasher.hash(password)    # XXX Does this automatically set a salt? 


def verify_pwd(given_password: str, actual_hash: str) -> bool:
    hasher = PasswordHash.recommended()
    return hasher.verify(given_password, actual_hash)