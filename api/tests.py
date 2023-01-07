import os
import csv

from django.test import TestCase
from django.core import management
from django.conf import settings

from .models import Channel, Content


class TestRating(TestCase):
    def setUp(self) -> None:
        channel = Channel.objects.create(
            id=123456,
            title='Test Channel',
            language='ch_CH',
            channel_image='/media/dummy.png'
        )
        content_1 = Content.objects.create(
            title='Test Content 1',
            description='Ignore this!',
            genre='action',
            content_file='/media/dummy.png',
            rating=3.56,
            channel=channel
        )
        content_2 = Content.objects.create(
            title='Test Content 2',
            description='Ignore this!',
            genre='action',
            content_file='/media/dummy.png',
            rating=6.13,
            channel=channel
        )
        management.call_command('rating')

    def test_average_ratings_calculation(self):
        """Average ratings for channels are accurately calculated"""
        static_files_path = os.path.join(settings.BASE_DIR, 'static_files')
        with open('{}/ratings.csv'.format(static_files_path)) as f:
            channel_ratings = [list(row.items()) for row in csv.DictReader(f, skipinitialspace=True)]
        self.assertEqual(int(channel_ratings[0][0][1]), 123456)
        self.assertEqual(round(float(channel_ratings[0][1][1]), 1), 4.8)
