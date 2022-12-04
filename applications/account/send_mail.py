from django.core.mail import send_mail


def send_activation_code(email, code):
    absolute_link = f'http://localhost:8000/account/activate/{code}'
    send_mail(
        'Письмо активации',
        absolute_link,
        'karimovbillal20002@gmail.com',
        [email]
    )
