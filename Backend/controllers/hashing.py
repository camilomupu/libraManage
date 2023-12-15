from passlib.context import CryptContext
from typing import List, Optional

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    
    @staticmethod
    def get_has_password(plain_password):
        return password_context.hash(plain_password)
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return password_context.verify(plain_password, hashed_password)