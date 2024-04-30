from app.settings import mail
from flask_mailman import EmailMessage

def init_app(app):
    mail.init_app(app)


def send_email(email_config: dict[str, any]) -> None:
    msg = EmailMessage(
        email_config.get('subject'), email_config.get('body'),
        'trashboyshub@gmail.com', [email_config.get('to')],
                       reply_to=['trashboyshub@gmail.com'])
    msg.content_subtype = 'html'
    msg.send()