from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'first_name', 'last_name', 'role'
        )
        read_only_field = ('role',)


class SignUpSerializer(serializers.Serializer):
    """Serializer для регистрации пользователя."""

    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=(validate_username,))
    email = serializers.EmailField(max_length=254,
                                   required=True)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,
                                     required=True,)
    confirmation_code = serializers.CharField(max_length=150,
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
    rating = serializers.IntegerField(read_only=True)

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
        queryset=Genre.objects.all()
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = (
            'title',
        )

    def validate(self, data):
        request = self.context['request']
        if (
            request.method == 'POST'
            and Review.objects.filter(
                author=request.user,
                title=get_object_or_404(
                    Title,
                    pk=self.context['view'].kwargs.get('title_id')
                )
            ).exists()
        ):
            raise serializers.ValidationError(
                'На это произведение уже есть отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
