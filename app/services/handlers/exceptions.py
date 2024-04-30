import traceback


def handle_exceptions(func):
    """
    Um decorador que trata exceções levantadas pela função decorada e retorna uma resposta com informações de erro apropriadas.

    Args:
        func (function): A função a ser decorada.

    Retorna:
        function: Uma função de embrulho que trata exceções levantadas pela função decorada 
            e retorna uma resposta com informações de erro apropriadas.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'details': traceback.format_exc(),
                'statuscode': 500
            }
    return wrapper