from app import create_app
from celery import Celery
from app.settings.env import load_rabbitmq_url

flask_app = create_app()

app = Celery(flask_app.import_name, broker=load_rabbitmq_url())
app.conf.update(flask_app.config)

if __name__ == '__main__':
    with flask_app.app_context():
        app.start()
