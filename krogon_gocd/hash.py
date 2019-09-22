import bcrypt


def hash_text(plaintext: str) -> str:
    return bcrypt.hashpw(plaintext.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
