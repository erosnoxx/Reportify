from uuid import UUID
from app.settings import db
from app.services import handle_exceptions
from sqlalchemy import inspect
from datetime import datetime, date
from app.models import Users


@handle_exceptions
def insert_database(model: object, payload: dict[str, any]) -> dict[str, any]:
    """
    Insere um elemento no banco de dados.

    Args:
        model (object): O modelo no qual o elemento será inserido.
        payload (dict): Um dicionário contendo os valores dos campos do elemento a ser inserido.

    Returns:
        dict[str, any]: Um dicionário indicando se a inserção foi bem-sucedida e, se não, uma mensagem de erro.
    """
    inspector = inspect_model_instance(model, payload)
    if not inspector.get('success'):
        return inspector
    
    element = model(**payload)
    db.session.add(element)
    db.session.commit()

    return {'success': True, 'message': 'Elemento criado', 'element': element.to_dict()}


@handle_exceptions
def get_element_database(model: object, field_to_search: str, field_value: any,
    return_element_instance: bool=False) -> dict[str, any]:
    """
    Obtém um elemento do banco de dados com base em um campo específico.

    Args:
        model (object): O modelo do qual o elemento será obtido.
        field_to_search (str): O nome do campo pelo qual o elemento será buscado.
        field_value (any): O valor do campo a ser buscado.
        return_element_instance (bool, optional): Se True, retorna a instância do elemento. False por padrão.

    Returns:
        dict[str, any]: Um dicionário indicando se a busca foi bem-sucedida e, se não, uma mensagem de erro.
    """
    element = model.query.filter_by(**{field_to_search: field_value}).first()

    if element is None:
        return {'success': False, 'message': 'Elemento não encontrado'}
    
    if return_element_instance:
        return {'success': True}, element
    
    return {'success': True, 'element': element.to_dict()}


def inspect_model_instance(model: object, payload: dict[str, any]) -> dict[str, any]:
    """
    Inspeciona uma instância de modelo para garantir que os valores dos campos correspondam aos tipos definidos.

    Args:
        model (object): O modelo a ser inspecionado.
        payload (dict): Um dicionário contendo os valores dos campos a serem verificados.

    Returns:
        dict[str, any]: Um dicionário indicando se a inspeção foi bem-sucedida e, se não, uma mensagem de erro.
    """
    inspector = inspect(model)
    column_info = {col.name: col.type for col in inspector.columns}

    for key, value in payload.items():
        is_valid, error_message = validate_column_value(column_info, key, value)
        if not is_valid:
            return {
                'success': False,
                'message': error_message,
            }
    return {'success': True}


def validate_column_value(column_info: dict[str, any], key: str, value: any) -> tuple[bool, str]:
    """
    Valida se o valor de uma coluna de um modelo corresponde ao seu tipo e tamanho.

    Args:
        column_info (dict): Um dicionário contendo informações sobre as colunas do modelo.
        key (str): A chave correspondente à coluna a ser validada.
        value (any): O valor a ser validado.

    Returns:
        tuple[bool, str]: Uma tupla indicando se a validação foi bem-sucedida e uma mensagem de erro, se aplicável.
    """
    if not isinstance(value, column_info[key].python_type):
        return False, f'O valor da coluna {key} não tem o tipo de dado correto'
    elif not isinstance(value, (date, datetime, int, UUID)):
        if column_info[key].length is not None and not len(value) <= column_info[key].length:
            return False, f'O valor da coluna {key} é maior do que o permitido'
    return True, None
