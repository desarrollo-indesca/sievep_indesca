from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

class Command(BaseCommand):
    help = "Carga las calderas de servicios industriales AMC"

    def handle(self, *args, **options):
        pass