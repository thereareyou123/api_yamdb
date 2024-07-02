from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import ValidationError

from users.constants import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_username

User = get_user_model()


class UserAdminSerializer(serializers.ModelSerializer):
    """Serializer для обработки запросов админа."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'first_name', 'last_name', 'role'
        )


class UserSerializer(UserAdminSerializer):
    """Serializer для обработки запросов пользователя."""

    class Meta(UserAdminSerializer.Meta):
        read_only_field = ('role',)


class SignUpSerializer(serializers.Serializer):
    """Serializer для регистрации пользователя."""

    username = serializers.CharField(max_length=NAME_MAX_LENGTH,
                                     required=True,
                                     validators=(validate_username,))
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH,
                                   required=True)

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        try:
            user, _ = User.objects.get_or_create(
                username=username,
                email=email
            )

        except IntegrityError:
            raise ValidationError(
                'Неверное сочетание имени пользователя и email'
            )
        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения для Yamdb',
            message=f'Ваш код: {confirmation_code}',
            from_email=settings.EMAIL_BACKEND,
            recipient_list=[user.email],
        )

        return user


class TokenSerializer(serializers.Serializer):
    """Serializer для проверки токена."""

    username = serializers.CharField(max_length=NAME_MAX_LENGTH,
                                     required=True,)
    confirmation_code = serializers.CharField(max_length=NAME_MAX_LENGTH,
                                              required=True,)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError('Введен неверный код подтверждения!')
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        allow_null=False,
        allow_empty=False
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        if (
            request.method == 'POST'
            and Review.objects.filter(
                author=request.user,
                title=title_id
            )
        ):
            raise serializers.ValidationError(
                'Вы уже оставили отзыв об этом произведении.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
