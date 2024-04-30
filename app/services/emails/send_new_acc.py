from celery import Celery
from flask import render_template
from app.settings.env import load_rabbitmq_url
from app.services import get_now


celery = Celery('app', broker=load_rabbitmq_url())


def send_new_acc_email(email_to_send: str, user_name: str):
    subject = 'Reportify - Confirmação de Troca de Senha'
    body = render_template('emails/auth/new_acc.html', now=get_now().strftime("%d - %B"),
        year=get_now().year, user_name=user_name)
    to = email_to_send

    email_config = {
        'subject': subject,
        'body': body,
        'to': to
    }

    result = celery.send_task('app.settings.tasks.email_sender',
        kwargs=email_config)
