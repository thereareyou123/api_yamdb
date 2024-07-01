from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import truncatechars

from api import constants
from reviews.constants import NAME, SLUG, MIN, MAX
from reviews.validators import validate_year

User = get_user_model()


class CategoryGenreBaseModel(models.Model):
    name = models.CharField('Название', max_length=NAME)
    slug = models.SlugField('Идентификатор', max_length=SLUG, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryGenreBaseModel):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Genre(CategoryGenreBaseModel):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ('name',)


class Title(models.Model):
    name = models.TextField('Название произведения', max_length=NAME)
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True,
        verbose_name='категория',
    )
    genre = models.ManyToManyField(
        Genre, through='TitleGenre',
        verbose_name='жанр'
    )
    year = models.SmallIntegerField('Год создания',
                                    validators=(validate_year,))

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('name',)

    def __str__(self):
        return truncatechars(self.name, constants.CUTTED_TITLE_SIZE)


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='произведение'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_combination_gt'
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(
                MIN,
                message='Оценка не может быть меньше чем 1'
            ),
            MaxValueValidator(
                MAX,
                message='Оценка не может быть больше чем 10'
            )
        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='review',
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Тело комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text
