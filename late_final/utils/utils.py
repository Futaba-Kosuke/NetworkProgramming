import hashlib

def sha256 (plain_text: str) -> str:
    return hashlib.sha256(plain_text.encode('utf-8')).hexdigest()

def sha256_add (secret_text: str, addition: str) -> str:
    return hashlib.sha256(f"{addition}{secret_text.encode('utf-8')}".encode('utf-8')).hexdigest()
