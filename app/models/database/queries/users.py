from app.models import Users
from app.models.database import (insert_database, get_element_database)
from app.services import (handle_exceptions, validate_sensitive_infos,
    validate_required_fields, pwd_hasher)


@handle_exceptions
def insert_user(payload: dict[str, any]) -> dict[str, any]:
    """
    Insere um usuário no banco de dados.

    Args:
        payload (dict): Um dicionário contendo os valores dos campos do usuário a ser inserido.

    Returns:
        dict[str, any]: Um dicionário indicando se a inserção foi bem-sucedida e, se não, uma mensagem de erro.
    """
    check_required_fields = validate_required_fields(
        ['first_name', 'last_name', 'email', 'password', 'date_of_birth'], payload, [], 'all')
    if not check_required_fields.get('success'):
        return check_required_fields

    check_sensitive_infos = check_sensitive_info({'email': payload.get('email'), 'password': payload.get('password')}, Users)

    if not check_sensitive_infos.get('success'):
        return check_sensitive_infos
    
    payload['password'] = pwd_hasher(payload.get('password'))

    user = insert_database(Users, payload)

    return user


@handle_exceptions
def get_user(field_to_search: str, field_value: any, return_instance: bool=False) -> dict[str, any]:
    """
    Obtém um usuário do banco de dados com base em um campo específico.

    Args:
        field_to_search (str): O campo pelo qual o usuário será obtido.

    Returns:
        dict[str, any]: Um dicionário indicando se a busca foi bem-sucedida e, se não, uma mensagem de erro.
    """

    return get_element_database(Users, field_to_search, field_value, return_instance)


def check_sensitive_info(fields_to_check: dict[str, any], model: object) -> dict[str, any]:
    """
    Verifica se informações sensíveis estão válidas para um modelo.

    Args:
        fields_to_check (dict): Um dicionário contendo as informações a serem verificadas.
        model (object): O modelo para o qual as informações serão verificadas.

    Returns:
        dict[str, any]: Um dicionário indicando se a verificação foi bem-sucedida e, se não, uma mensagem de erro.
    """
    are_infos_valid = validate_sensitive_infos(fields_to_check, model)
    if not are_infos_valid.get('success'):
        return are_infos_valid
    return {'success': True}
