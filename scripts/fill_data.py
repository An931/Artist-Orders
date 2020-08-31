from apps.masterpieces.factories import MasterpieceFactory
from apps.offers.factories import OfferFactory
from apps.orders.factories import OrderFactory
from apps.reports.factories import (
    MasterpieceReportFactory,
    OrderReportFactory,
    UserReportFactory
)
from apps.tags.factories import TagFactory
from apps.users.factories import ArtistFactory, CustomerFactory

TAGS_COUNT = 5
ARTISTS_COUNT = 3
CUSTOMERS_COUNT = 3
ORDER_INFOS_COUNT = 5
MASTERPIECES_COUNT = 10
ORDERS_COUNT = 5
USER_REPORTS_COUNT = 3
ORDER_INFO_REPORTS_COUNT = 3
MASTERPIECE_REPORTS_COUNT = 3
OFFERS_COUNT = 5


def run():
    """Fill db by random data of every type."""
    add_tags()
    add_users()
    add_orders()
    add_masterpieces()
    add_user_reports()
    add_order_reports()
    add_masterpiece_reports()


def add_tags():
    """Add test tags to db."""
    tags = TagFactory.create_batch(TAGS_COUNT)
    for tag in tags:
        print(f'Tag created: {tag.title}')


def add_users():
    """Add test users to db."""
    users = CustomerFactory.create_batch(CUSTOMERS_COUNT)
    users += ArtistFactory.create_batch(ARTISTS_COUNT)

    for user in users:
        print(
            f'User created: id: {user.id}, {user.get_full_name()} '
            f'{user.role} {user.email}'
        )


def add_orders():
    """Add test order infos to db."""
    orders = OrderFactory.create_batch(ORDER_INFOS_COUNT)
    for order in orders:
        print(
            f'Order info created: id: {order.id}, '
            f'creator: {order.created_by}'
        )


def add_masterpieces():
    """Add test masterpieces to db."""
    masterpieces = MasterpieceFactory.create_batch(MASTERPIECES_COUNT)
    for masterpiece in masterpieces:
        print(
            f'Masterpiece created: id: {masterpiece.id} '
            f'artist: {masterpiece.artist}'
        )


def add_user_reports():
    """Add test user reports to db."""
    reports = UserReportFactory.create_batch(USER_REPORTS_COUNT)
    for report in reports:
        print(
            f'Report to user created: id: {report.id}, '
            f'creator: {report.created_by}, '
            f'to user: {report.user}'
        )


def add_order_reports():
    """Add test order reports to db."""
    reports = OrderReportFactory.create_batch(ORDER_INFO_REPORTS_COUNT)
    for report in reports:
        print(
            f'Report to order info created: id: {report.id}, '
            f'creator: {report.created_by}, '
            f'to order info: {report.order}'
        )


def add_masterpiece_reports():
    """Add test masterpiece reports to db."""
    reports = MasterpieceReportFactory.create_batch(MASTERPIECE_REPORTS_COUNT)
    for report in reports:
        print(
            f'Report to masterpiece created: id: {report.id}, '
            f'creator: {report.created_by}, '
            f'to masterpiece: {report.masterpiece}'
        )


def add_offers():
    """Add test offers to db."""
    offers = OfferFactory.create_batch(OFFERS_COUNT)
    for offer in offers:
        print(
            f'Offer created: id: {offer.id}, '
            f'order: {offer.order}, '
            f'artist: {offer.artist}'
        )
