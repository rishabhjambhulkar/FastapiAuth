from passlib.context import CryptContext




pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd.hash(password)
