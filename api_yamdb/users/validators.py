import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        msg = 'Имя пользователя "me" использовать нельзя'
        raise ValidationError(msg)
    if not re.match(r'[\w.@+-]+\Z$', value):
        raise ValidationError(
            'Разрешается использовать только буквы, цифры и символы @/./+/-/_'
        )
