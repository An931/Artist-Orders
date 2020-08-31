from celery.decorators import task

from django.core.mail import send_mail


@task(name='send_offer_task')
def send_offer_task(customer_mail):
    """Send an email to customer when he have new offer"""

    return send_mail(
            'New offer!',
            f'Artist added new offer to your order. Check it.',
            'art-orders@mail.ru',
            [customer_mail],
        )
