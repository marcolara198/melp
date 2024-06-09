from django.core.management.base import BaseCommand

from api.management.commands.importer import Importer


class Command(BaseCommand):
    help = 'Imports the legacy records'

    def handle(self, *args, **options):
        Importer().import_all()
