# Reportify

Este é um breve guia sobre como configurar e executar o projeto em um ambiente local, tanto no Linux quanto no Windows.

## Instalação

### Pré-requisitos

- Python 3.x
- `make` (opcional, apenas para Linux)
- Ambiente virtual (recomendado)
- PostgreSQL (ou outro banco de dados configurado)

### Passos de instalação

1. Clone o repositório para o seu computador:

```bash
git clone git@github.com:erosnoxx/Reportify.git
cd Reportify
```

2. Crie e ative um ambiente virtual:

```bash
# No Linux
python3 -m venv venv
source venv/bin/activate

# No Windows
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependências do projeto:

```bash
# No Linux
make install

# No Windows
pip install -r requirements.txt
```

4. Realize as migrações do banco de dados:

```bash
# Inicialize as migrações
flask db init

# Crie as migrações
flask db migrate

# Edite o arquivo env.py dentro da pasta migrations e adicione a linha 'from app.models import *' no início do arquivo

# Aplique as migrações
flask db upgrade
```

5. Crie um arquivo `.env` baseado no arquivo `.envsample` e configure as variáveis de ambiente conforme necessário.

## Executando o Projeto

### Servidor Web (Gunicorn)

Para iniciar o servidor web, execute o seguinte comando:

```bash
# No Linux
make run
```

No Windows, você pode executar diretamente os comandos Python:

```bash
gunicorn -c gunicorn_conf.py "app:create_app()"
```

### Celery

Para iniciar o Celery, é necessário abrir um terminal separado e executar:

```bash
# No Linux
make celery
```

No Windows, você pode executar diretamente os comandos Python:

```bash
celery -A app.settings.tasks worker --loglevel=INFO
```

Certifique-se de que o ambiente virtual esteja ativado antes de executar esses comandos.
