import csv

from django.core.management.base import BaseCommand
from questionnaire.models import Country, Region


class Command(BaseCommand):
    args = 'name_of_the_csv.file'
    help = 'Populates locations from a csv file'

    def handle(self, *args, **kwargs):
        csv_file = csv.reader(open(args[0], "rb"))
        skip_headers = csv_file.next()
        for locations in csv_file:
            region = Region.objects.get_or_create(name=locations[0])[0]
            Country.objects.get_or_create(name=locations[-1], region=region)
        self.stdout.write('Successfully imported!')