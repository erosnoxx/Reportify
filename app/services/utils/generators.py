import pytz
import pyotp
import random
from datetime import datetime
from uuid import uuid4


def get_now() -> datetime:
    """
    Retorna a data e hora atual no fuso horário de São Paulo.

    Returns:
        datetime: Objeto datetime representando a data e hora atual no fuso horário de São Paulo.
    """
    return datetime.now(pytz.timezone('America/Sao_Paulo'))


def generate_uuid() -> str:
    """
    Gera um UUID (Identificador Único Universal).

    Returns:
        str: Uma string representando o UUID gerado.
    """
    return uuid4()


def generate_otp_code() -> str:
    """
    Gera um código OTP baseado em tempo (TOTP)

    Returns:
        str: Uma string contendo um código OTP.
    """
    return pyotp.TOTP(pyotp.random_base32(), digits=6).now()
