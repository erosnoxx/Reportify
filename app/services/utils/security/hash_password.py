from werkzeug.security import generate_password_hash, check_password_hash


def pwd_hasher(password: str) -> str:
    """
    Gera o hash de uma senha utilizando o algoritmo Argon2.

    Args:
        password (str): A senha a ser hasheada.

    Returns:
        str: O hash resultante da senha.
    """
    return generate_password_hash(password, method='pbkdf2:sha256')


def check_hashed_pwd(hashed_pwd: str, password: str) -> bool:
    """
    Verifica se uma senha corresponde ao seu hash utilizando o algoritmo Argon2.

    Args:
        hashed_pwd (str): O hash da senha a ser verificado.
        password (str): A senha fornecida para verificação.

    Returns:
        bool: True se a senha fornecida corresponder ao hash, False caso contrário.
    """
    return check_password_hash(hashed_pwd, password)
