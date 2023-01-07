import os
import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Avg
from django.db.models.functions import Round

from ...models import Content


class Command(BaseCommand):
    help = 'Calculates average rating of channels and exports to csv file.'

    def handle(self, *args, **options):
        channel_ratings = Content.objects.filter(rating__isnull=False) \
            .values('channel__id') \
            .annotate(avg_rating=Round(Avg('rating'), 2)) \
            .order_by('-avg_rating')

        static_files_path = os.path.join(settings.BASE_DIR, 'static_files')
        with open('{}/ratings.csv'.format(static_files_path), 'w+', encoding='utf8', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, channel_ratings[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(channel_ratings)

        self.stdout.write(self.style.SUCCESS('Successfully calculated and exported average ratings.'))
