from csv import DictReader

from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


class Command(BaseCommand):
    help = 'Command to automatically populate the database'

    def load_users(self):
        for row in DictReader(
                open('static/data/users.csv', encoding='UTF-8')):
            User.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS(
            'users.csv выгружен в бд.')
        )

    def load_category(self):
        for row in DictReader(
                open('static/data/category.csv', encoding='UTF-8')):
            Category.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS(
            'category.csv выгружен в бд.')
        )

    def load_genre(self):
        for row in DictReader(
                open('static/data/genre.csv', encoding='UTF-8')):
            Genre.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS(
            'genre.csv выгружен в бд.')
        )

    def load_title(self):
        for row in DictReader(
                open('static/data/titles.csv', encoding='UTF-8')):
            Title.objects.get_or_create(
                category=Category.objects.get(id=row.pop('category')), **row)

        self.stdout.write(self.style.SUCCESS(
            'titles.csv выгружен в бд.')
        )

    def load_genre_title(self):
        for row in DictReader(
                open('static/data/genre_title.csv')):
            TitleGenre.objects.get_or_create(
                title=Title.objects.get(id=row.pop('title_id')),
                genre=Genre.objects.get(id=row.pop('genre_id')))

        self.stdout.write(self.style.SUCCESS(
            'genre_title.csv выгружен в бд.')
        )

    def load_review(self):
        for row in DictReader(
                open('static/data/review.csv', encoding='UTF-8')):
            Review.objects.get_or_create(
                title=Title.objects.get(id=row.pop('title_id')),
                author=User.objects.get(id=row.pop('author')),
                **row)

        self.stdout.write(self.style.SUCCESS(
            'review.csv выгружен в бд.')
        )

    def load_comments(self):
        for row in DictReader(
                open('static/data/comments.csv', encoding='UTF-8')):
            Comment.objects.get_or_create(
                review=Review.objects.get(id=row.pop('review_id')),
                author=User.objects.get(id=row.pop('author')),
                **row)

        self.stdout.write(self.style.SUCCESS(
            'comments.csv выгружен в бд.')
        )

    def handle(self, *args, **options):
        try:
            self.load_category()
            self.load_genre()
            self.load_title()
            self.load_genre_title()
            self.load_users()
            self.load_review()
            self.load_comments()

        except IntegrityError as err:
            self.stdout.write(self.style.ERROR(
                f'ERROR - {err}')
            )
            exit()
