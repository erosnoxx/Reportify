from datetime import datetime, date

def convert_str_to_date(date: str) -> date:
    """
    Valida se a string fornecida é uma data no formato 'YYYY-MM-DD'.

    Tenta converter a string de data fornecida para um objeto date. Se a conversão for bem-sucedida,
    retorna o objeto date. Caso contrário, retorna um dicionário indicando falha na validação.

    Parâmetros:
    - date (str): A string da data para validar.
    - model (object, opcional): Um modelo de banco de dados, não utilizado nesta função mas incluído para compatibilidade de interface.

    Retorna:
    - date: Um objeto date se a string de data for válida.
    - bool: Caso falhe, retorna False.
    """
    try:
        return datetime.strptime(date, '%Y-%m-%d').date()
    except:
        return False
