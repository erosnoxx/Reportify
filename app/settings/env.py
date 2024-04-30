import os
from dotenv import load_dotenv

load_dotenv('.env')


def init_app(app) -> None:
    """
    Inicializa as configurações do aplicativo Flask.

    Esta função carrega as configurações do ambiente a partir do arquivo '.env' e configura
    o aplicativo Flask de acordo com essas configurações.

    Args:
        app (Flask): Instância do aplicativo Flask a ser configurado.

    Returns:
        None

    Configurações do Aplicativo:
        - STATIC_FOLDER: Define o diretório para arquivos estáticos.
        - TEMPLATE_FOLDER: Define o diretório para os modelos HTML.
        - SECRET_KEY: Define a chave secreta para sessões.
        - FLASK_DEBUG: Define se o modo de depuração do Flask está ativado.
        - FLASK_ENV: Define o ambiente de execução do Flask.
        - FLASK_APP: Define o módulo Flask principal.
        - SQLALCHEMY_TRACK_MODIFICATIONS: Define se o rastreamento de modificações no SQLAlchemy está ativado.
        - TESTING: Define se o aplicativo está em modo de teste.

    Configurações do Banco de Dados:
        - SQLALCHEMY_DATABASE_URI: Define a URI do banco de dados SQLAlchemy.
        - Para o modo de teste, usa um banco de dados SQLite em memória.

    Configurações do Pool do Postgres:
        - Define as opções do pool do SQLAlchemy se uma URI de banco de dados Postgres for fornecida.

    Configurações do Redis:
        - REDIS_URL: Define a URL do servidor Redis.
    """

    # App configurations

    app.static_folder = os.environ.get('STATIC_FOLDER')
    app.template_folder = os.environ.get('TEMPLATE_FOLDER')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['FLASK_DEBUG'] = os.environ.get('FLASK_DEBUG')
    app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV')
    app.config['FLASK_APP'] = os.environ.get('FLASK_APP')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    if 'PYTEST_CURRENT_TEST' in os.environ:
        app.config['TESTING'] = True

    # Database configurations

    db_service = os.environ.get('DB_SERVICE')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = f"{db_service}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"  

    if app.config['TESTING']:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    
    # Postgres pool configurations

    if app.config['SQLALCHEMY_DATABASE_URI'] == f"{db_service}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}":
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': int(os.environ.get('POOL_SIZE')),
            'max_overflow': int(os.environ.get('MAX_OVERFLOW')),
            'pool_timeout': int(os.environ.get('POOL_TIMEOUT')),
            'pool_recycle': int(os.environ.get('POOL_RECYCLE')),
            'pool_pre_ping': True
        }

    # Redis configurations

    redis_host = os.environ.get('REDIS_HOST')
    redis_port = os.environ.get('REDIS_PORT')
    redis_database = os.environ.get('REDIS_DATABASE')

    app.config['REDIS_URL'] = f"redis://{redis_host}:{redis_port}/{redis_database}"

    # Email configurations

    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True


def load_rabbitmq_url() -> str:
    
    rabbitmq_user = os.environ.get('RABBITMQ_USER')
    rabbitmq_password = os.environ.get('RABBITMQ_PASSWORD')
    rabbitmq_host = os.environ.get('RABBITMQ_HOST')
    rabbitmq_port = int(os.environ.get('RABBITMQ_PORT'))

    return f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}"
