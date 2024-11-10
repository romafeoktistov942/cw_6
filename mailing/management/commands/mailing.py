from django.core.management import BaseCommand

from mailing.services import get_mailings


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Ручной запуск рассылки"""

        get_mailings()
