from passlib.context import CryptContext

# Configuramos bcrypt como el algoritmo de hashing principal
# "deprecated='auto'" permite que si en el futuro bcrypt se actualiza, 
# el sistema pueda leer hashes viejos pero cree los nuevos con la versión segura.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Comprueba si la contraseña en texto plano coincide con el hash guardado.
    Se usará en el Login.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Genera un hash seguro a partir de una contraseña en texto plano.
    Se usará en el Registro.
    """
    return pwd_context.hash(password)