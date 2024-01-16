from django.contrib import admin
from tinyapp.models import ShortenedURLStore,User

# Register your models here.
admin.site.register(ShortenedURLStore)
admin.site.register(User)
