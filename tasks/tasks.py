from mysite.celery import app
from django.core.mail import send_mail

@app.task
def send_auth_mail(user_email):
    send_mail(
        'Добро пожаловать в Wunderlist Reborn!',
        'Мы очень рады Вас видеть!',
        'wunderlistapp228@gmail.com',
        [user_email],
        fail_silently=False,
    )