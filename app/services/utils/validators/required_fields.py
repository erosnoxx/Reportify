from app.services.handlers.exceptions import handle_exceptions

def remove_ignored_fields(required_fields: list[str], fields_to_ignore: list[str]) -> list[str]:
    """
    Remove os campos a serem ignorados da lista de campos obrigatórios.

    Args:
        required_fields (list[str]): Lista dos campos obrigatórios.
        fields_to_ignore (list[str]): Lista de campos a serem ignorados.

    Returns:
        list[str]: Lista dos campos obrigatórios sem os campos ignorados.
    """
    for field in fields_to_ignore:
        if field in required_fields:
            required_fields.remove(field)
    return required_fields


def find_missing_fields(required_fields: list[str], fields_to_check: dict[str, any]) -> list[str]:
    """
    Encontra os campos obrigatórios ausentes nos campos a serem verificados.

    Args:
        required_fields (list[str]): Lista dos campos obrigatórios.
        fields_to_check (dict[str, any]): Dicionário contendo os campos a serem verificados.

    Returns:
        list[str]: Lista dos campos obrigatórios que estão ausentes nos campos verificados.
    """
    return [field for field in required_fields if field not in fields_to_check]


def validate_any(required_fields: list[str], fields_to_check: dict[str, any],
    missing_fields: list[str]) -> dict[str, any]:
    """
    Valida se pelo menos um campo obrigatório está presente nos campos verificados.

    Args:
        required_fields (list[str]): Lista dos campos obrigatórios.
        fields_to_check (dict[str, any]): Dicionário contendo os campos a serem verificados.
        missing_fields (list[str]): Lista dos campos obrigatórios ausentes nos campos verificados.

    Returns:
        dict[str, any]: Um dicionário contendo informações sobre o resultado da validação.
            - 'success' (bool): True se pelo menos um campo obrigatório estiver presente, False caso contrário.
            - 'message' (str): A mensagem indicando o resultado da validação.
    """
    if not len(missing_fields) == len(required_fields):
        present_fields = [field for field in required_fields if field in fields_to_check]
        return {'success': True, 'message': f'Campos presentes: {present_fields}'}
    return {'success': False, 'message': 'Todos os campos obrigatórios ausentes'}


def validate_all(required_fields: list[str], fields_to_check: dict[str, any],
    missing_fields: list[str]) -> dict[str, any]:
    """
    Valida se todos os campos obrigatórios estão presentes nos campos verificados.

    Args:
        required_fields (list[str]): Lista dos campos obrigatórios.
        fields_to_check (dict[str, any]): Dicionário contendo os campos a serem verificados.
        missing_fields (list[str]): Lista dos campos obrigatórios ausentes nos campos verificados.

    Returns:
        dict[str, any]: Um dicionário contendo informações sobre o resultado da validação.
            - 'success' (bool): True se todos os campos obrigatórios estiverem presentes, False caso contrário.
            - 'message' (str): A mensagem indicando o resultado da validação.
    """
    if not missing_fields and len(fields_to_check.keys()) == len(required_fields):
        return {'success': True}
    return {'success': False, 'message': 'Todos os campos obrigatórios ausentes'}


@handle_exceptions
def validate_required_fields(required_fields: list[str], fields_to_check: dict[str, any],
                              fields_to_ignore: list[str] = [], validation_type: str = 'all') -> dict[str, any]:
    """
    Valida se os campos obrigatórios estão presentes nos campos a serem verificados.

    Args:
        required_fields (list[str]): Lista dos campos obrigatórios.
        fields_to_check (dict[str, any]): Dicionário contendo os campos a serem verificados.
        fields_to_ignore (list[str], opcional): Lista de campos a serem ignorados na validação. Padrão é [].
        validation_type (str, opcional): Tipo de validação a ser realizada ('all' para todos os campos obrigatórios
            ou 'any' para pelo menos um campo obrigatório). Padrão é 'all'.

    Returns:
        dict[str, any]: Um dicionário contendo informações sobre o resultado da validação.
            - 'success' (bool): True se a validação for bem-sucedida, False caso contrário.
            - 'message' (str): A mensagem indicando o resultado da validação.
    """
    if validation_type not in ['any', 'all']:
        return {'success': False, 'message': 'validation_type tem que ser "all" ou "any"'}

    required_fields = remove_ignored_fields(required_fields, fields_to_ignore)
    missing_fields = find_missing_fields(required_fields, fields_to_check)

    if validation_type == 'any':
        return validate_any(required_fields, fields_to_check, missing_fields)
    elif validation_type == 'all':
        return validate_all(required_fields, fields_to_check, missing_fields)
