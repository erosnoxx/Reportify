import re
from app.services.utils.validators.required_fields import validate_required_fields


EMAIL_REGEX = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?<!\.)$'
PASSWORD_REGEX = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$!%^&+=_\-()])\S{8,}$"


def validate_infos(value: str, regex: str) -> bool:
    """
    Valida se o valor corresponde ao padrão de expressão regular fornecido.

    Args:
        value (str): O valor a ser validado.
        regex (str): A expressão regular a ser usada para validação.

    Returns:
        bool: True se o valor corresponder ao padrão, False caso contrário.
    """
    if not isinstance(value, str) or not isinstance(regex, str):
        return False
    
    return bool(re.match(regex, value))


def check_regex(info_to_validate: str, infos_to_validate: dict[str, any],
                regex: str, error_msg: str) -> list[str]:
    """
    Verifica se o valor correspondente à chave especificada em infos_to_validate corresponde ao padrão de expressão regular fornecido.

    Args:
        info_to_validate (str): A chave que contém o valor a ser validado em infos_to_validate.
        infos_to_validate (dict[str, any]): O dicionário de informações a ser validado.
        regex (str): A expressão regular a ser usada para validação.
        error_msg (str): A mensagem de erro a ser retornada caso a validação falhe.

    Returns:
        list[str]: Uma lista contendo a mensagem de erro se a validação falhar, caso contrário, uma lista vazia.
    """
    errors = []
    if info_to_validate in infos_to_validate:
        if not validate_infos(infos_to_validate.get(info_to_validate), regex):
            errors.append(error_msg)
    return errors


def check_existence(info_to_validate: str, infos_to_validate: dict[str, any],
                    model: object, error_msg: str) -> list[str]:
    """
    Verifica se o valor correspondente à chave especificada em infos_to_validate já existe no banco de dados.

    Args:
        info_to_validate (str): A chave que contém o valor a ser validado em infos_to_validate.
        infos_to_validate (dict[str, any]): O dicionário de informações a ser validado.
        model (object): O modelo de dados a ser consultado no banco de dados.
        error_msg (str): A mensagem de erro a ser retornada caso a validação falhe.

    Returns:
        list[str]: Uma lista contendo a mensagem de erro se a validação falhar, caso contrário, uma lista vazia.
    """
    errors = []
    if info_to_validate in infos_to_validate:
        if model and model.query.filter_by(**{info_to_validate: infos_to_validate.get(info_to_validate)}).first() is not None:
            errors.append(error_msg)
    return errors


def check_required_fields(infos_to_check: dict[str, any]) -> dict[str, any]:
    """
    Verifica se os campos obrigatórios estão presentes nos campos a serem verificados.

    Args:
        infos_to_check (dict[str, any]): Dicionário contendo os campos a serem verificados.

    Returns:
        dict[str, any]: Um dicionário contendo informações sobre o resultado da validação.
            - 'success' (bool): True se pelo menos um campo obrigatório estiver presente, False caso contrário.
            - 'message' (str): A mensagem indicando o resultado da validação.
                Se a validação for bem-sucedida, a mensagem informa os campos presentes.
                Se a validação falhar, a mensagem informa que todos os campos obrigatórios estão ausentes.
    """
    return validate_required_fields(
        ['email', 'password'],
        infos_to_check, [], 'any')


def validate_sensitive_infos(infos_to_validate: dict[str, any], model: object=None) -> dict[str, any]:
    """
    Valida informações sensíveis, como e-mail, CPF e CNPJ.

    Args:
        infos_to_validate (dict[str, any]): O dicionário de informações a ser validado.
        model (object, opcional): O modelo de dados a ser consultado no banco de dados. Padrão é None.

    Returns:
        dict[str, any]: Um dicionário contendo informações sobre o resultado da validação.
            - 'success' (bool): True se a validação for bem-sucedida, False caso contrário.
            - 'message' (str): A mensagem de sucesso ou erro da validação.
            - 'errors' (list[str]): Uma lista de mensagens de erro, se houver.
    """
    if not isinstance(infos_to_validate, dict):
        return {
           'success': False,
           'message': 'Informações inválidas',
        }
    
    if len(infos_to_validate) > 6:
        return {'success': False, 'message': 'Mais campos do que o requerido'}

    are_fields_valid = check_required_fields(infos_to_validate)
    if not are_fields_valid.get('success'):
            return are_fields_valid

    errors = []

    if 'email' in infos_to_validate.keys():
        errors.extend(check_existence('email', infos_to_validate, model, 'E-mail em uso'))
        errors.extend(check_regex('email', infos_to_validate, EMAIL_REGEX, 'E-mail inválido'))

    if 'password' in infos_to_validate.keys():
        errors.extend(check_regex('password', infos_to_validate, PASSWORD_REGEX, 'Senha inválida'))

    if errors:
        return {
            'success': False,
            'message': 'Campo(s) informado(s) inválido(s)',
            'errors': errors
        }

    return {'success': True}
