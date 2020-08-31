from celery.task.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import send_mail
from .models import User
from .strings import ARTIST_ROLE
from ..orders.models import Order


@periodic_task(run_every=(crontab(minute=0, hour=9)), name="send_top_orders")
def send_top_orders():
    """Send top of orders for artists every day"""

    orders_count = 10
    artists_mails = [d['email'] for d in
                     User.objects.filter(role=ARTIST_ROLE).values('email')]
    top_open_orders = Order.objects.filter(offer__isnull=True).order_by(
        '-views')[:orders_count]
    orders_titles = [d['title'] for d in
                     top_open_orders.values('title')]

    subject = 'Top orders today!'
    titles_str = '\n'.join(orders_titles)
    message = f'This orders are waiting for you:\n\n{titles_str}'
    return send_mail(
        subject,
        message,
        'art-orders@mail.ru',
        artists_mails,
    )
