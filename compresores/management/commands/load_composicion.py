from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from intercambiadores.models import Planta
from compresores.models import *
import csv
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Load compressors from data/compresores.csv into the database. ONLY THE FIRST CASE."

    def handle(self, *args, **options):
        COMPUESTOS = []
        with transaction.atomic():
            try:
            except Exception as e:
                raise CommandError(f"Error loading compressors: {e}")
