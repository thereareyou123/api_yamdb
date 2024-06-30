import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)

TABLES = {
    Category: 'category.csv',
    Comment: 'comments.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Title: 'titles.csv',
    TitleGenre: 'genre_title.csv',
    User: 'users.csv',
}


class Command(BaseCommand):
    help = 'Command to automatically populate the database'

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_f}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
