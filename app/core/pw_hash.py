from passlib.context import CryptContext

password_context = CryptContext(schemes=["argon2","bcrypt"],deprecated="auto") 


def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(
        plain_password: str, # from request 
        hashed_password: str # from db
        )-> bool:
    
    return password_context.verify(plain_password, hashed_password)   