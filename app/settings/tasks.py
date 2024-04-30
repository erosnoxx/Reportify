from app.settings.management.mail import send_email
from celery_worker import app, flask_app


@app.task(bind=True, retry_backoff=3, max_retries=3)
def email_sender(self, subject, body, to) -> None:
    with flask_app.app_context():
        try:
            email_config = {
                'subject': subject,
                'body': body,
                'to': to
            }
            send_email(email_config=email_config)
        except Exception as exc:
            self.retry(exc=exc)