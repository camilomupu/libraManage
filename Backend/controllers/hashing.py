from passlib.context import CryptContext
from typing import List, Optional

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher:
    """
    Clase de utilidad para el manejo de contraseñas.
    Methods:
        get_has_password(plain_password: str) -> str:
            Genera un hash para una contraseña dada.
        verify_password(plain_password: str, hashed_password: str) -> bool:
            Verifica si una contraseña coincide con su hash correspondiente.
    """
    @staticmethod
    def get_has_password(plain_password):
        """
        Genera un hash para una contraseña dada.
        Args:
            plain_password (str): Contraseña en texto plano.
        Returns:
            str: Hash de la contraseña.
        """
        return password_context.hash(plain_password)
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verifica si una contraseña coincide con su hash correspondiente.
        Args:
            plain_password (str): Contraseña en texto plano.
            hashed_password (str): Hash de la contraseña.
        Returns:
            bool: True si la contraseña coincide, False si no.
        """
        return password_context.verify(plain_password, hashed_password)