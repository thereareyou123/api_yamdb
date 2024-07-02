import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import (
    Category, Genre, Title, TitleGenre, Review, Comment
)
from users.models import User

from api_yamdb.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Command to automatically populate the database'

    def handle(self, *args, **options):

        TABLES = {
            Category: 'category.csv',
            Comment: 'comments.csv',
            Genre: 'genre.csv',
            Review: 'review.csv',
            Title: 'titles.csv',
            TitleGenre: 'genre_title.csv',
            User: 'users.csv',
        }

        for model, csv_f in TABLES.items():
            with open(f'{BASE_DIR}/static/data/{csv_f}',
                      'r', encoding='utf8') as file:
                cvs_rows = csv.DictReader(file, delimiter=',')
                for row in cvs_rows:
                    shallow_copy = row.copy()
                    for keys in shallow_copy.keys():
                        if 'category' in keys:
                            row['category_id'] = row.pop('category')
                        elif 'author' in keys:
                            row['author_id'] = row.pop('author')
                    try:
                        model.objects.create(**row)
                    except ValueError as e:
                        raise CommandError(
                            f'Ошибка: {e}, файл {csv_f}, строка {row}'
                        )
            self.stdout.write(
                f'Данные из таблицы {model.__name__} импортированы!')
