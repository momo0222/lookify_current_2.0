import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import School

class Command(BaseCommand):
    help = 'Import public and private schools from CSV files'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join(settings.BASE_DIR, 'data')
        public_schools_path = os.path.join(data_dir, 'Public_Schools.csv')
        print(public_schools_path)
        private_schools_path = os.path.join(data_dir, 'Private_Schools.csv')
        self.stdout.write('Starting import...')
        self.import_schools(public_schools_path)
        self.stdout.write('imported public')
        self.import_schools(private_schools_path)
        self.stdout.write('imported private')
    
    def import_schools(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                School.objects.create(
                    name=row['NAME'],
                    address=row['ADDRESS'],
                    city=row['CITY'],
                    state=row['STATE'],
                    zip_code=row['ZIP'],
                    country="USA"
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully imported schools from {file_path}'))
