import os
from dotenv import load_dotenv

load_dotenv('.env')

def get_env():
    """
    Retorna as variáveis de ambiente necessárias para rodar a aplicação flask
    """
    return {           # Enables debug mode
        "FLASK_ENV": os.environ.get('FLASK_ENV'),
        "FLASK_APP": os.environ.get('FLASK_APP'),
        "SECRET_KEY": os.environ.get('SECRET_KEY'),
        "DB_SERVICE":os.environ.get('DB_SERVICE'),
        "DB_USER": os.environ.get('DB_USER'),
        "DB_PASSWORD": os.environ.get('DB_PASSWORD'),
        "DB_HOST": os.environ.get('DB_HOST'),
        "DB_PORT": os.environ.get('DB_PORT'),
        "DB_NAME": os.environ.get('DB_NAME'),
        "REDIS_HOST": os.environ.get('REDIS_HOST'),
        "REDIS_PORT": os.environ.get('REDIS_PORT'),
        "REDIS_DATABASE": os.environ.get('REDIS_DATABASE'),
        "POOL_SIZE": str(os.environ.get('POOL_SIZE')),
        "MAX_OVERFLOW": str(os.environ.get('MAX_OVERFLOW')),
        "POOL_TIMEOUT": str(os.environ.get('POOL_TIMEOUT')),
        "POOL_RECYCLE": str(os.environ.get('POOL_RECYCLE')),
        "POOL_PRE_PING": os.environ.get('POOL_PRE_PING')
    }

def worker_init(worker):
    """
    Inicia o processo do worker com as variáveis de ambiente.

    Essa função é chamada para setar as variáveis de ambiente para o processo do worker.
    Ela recupera as variáveis de ambiente de um dicionário retornado pela função 'get_env' e as define para o processo do worker,
    garantindo que o worker tenha todas as configurações necessárias para rodar corretamente.
    """
    env = get_env()
    for key, value in env.items():
        os.environ[key] = value

def post_fork(server, worker):
    worker_init(worker)

def when_ready(server):
    worker_init(server)

bind = os.environ.get('BIND')
workers = int(os.environ.get('WORKERS'))
worker_class = os.environ.get('WORKER_CLASS')
worker_connections = int(os.environ.get('WORKER_CONNECTIONS'))
