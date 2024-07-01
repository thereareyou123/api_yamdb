from django.utils import timezone
from rest_framework import serializers


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise serializers.ValidationError(
            'Нельзя добавлять произведения, которые еще не вышли')
