import hashlib
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from tinyapp.models import ShortenedURLStore


def generate_url(url, custom_url=None):
    if custom_url:
        custom_url = custom_url
        return custom_url
    else:
        md5_hash = hashlib.md5(url.encode()).hexdigest()
        short_url = md5_hash[:5]
        return short_url


def shorten_url(original_url, custom_url):
    if original_url:
        if custom_url:
            shortened_url = generate_url(original_url, custom_url)
        else:
            shortened_url = generate_url(original_url)
        return shortened_url
    else:
        raise ValidationError(
            {
                "title": "TinyUrl",
                "message": "Please provide a valid URL",
            }
        )


def find_url(tiny_url):
    try:
        shortened_url = ShortenedURLStore.objects.get(custom_url=tiny_url)
        return shortened_url.original_url
    except ObjectDoesNotExist:
        raise ValueError("Tiny URL not found.")
