from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tinyapp.models import ShortenedURLStore
from common.utils import validate_url
from common.func import shorten_url, find_url


class TinySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURLStore
        fields = [
            "original_url",
            "custom_url",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data

        if not validate_url(data.get("original_url")):
            raise ValidationError(
                {
                    "title": "Tiny",
                    "message": "Invalid url",
                },
            )

        original = ShortenedURLStore.objects.filter(
            original_url=data.get("original_url")
        ).first()
        if original:
            raise ValidationError(
                {
                    "title": "TinyUrl",
                    "message": "Original URL  already exists in the database",
                }
            )

        custom = ShortenedURLStore.objects.filter(
            custom_url=data.get("custom_url")
        ).first()
        if custom:
            raise ValidationError(
                {
                    "title": "TinyUrl",
                    "message": "Custom URL  already exists in the database",
                }
            )

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        input_url = validated_data.get("original_url")
        custom_url = validated_data.get("custom_url")
        shortened_url = shorten_url(input_url, custom_url)
        if custom_url:
            tiny = super().create(validated_data)
        else:
            tiny = super().create(validated_data)
            tiny.custom_url = shortened_url
            tiny.save()
        return tiny
    
