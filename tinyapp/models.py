from django.db import models
from django.utils.timezone import now
from uuid import uuid4
class ShortenedURLStore(models.Model):
    original_url = models.URLField(max_length=2000, unique=True)
    custom_url = models.CharField(max_length=50, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"ShortenedURL: {self.original_url}--{self.created_at}"

class User(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    full_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, verbose_name="email address")
    password = models.CharField(max_length=50,null=False)
    def __str__(self):
        return self.full_name 
    class Meta:
        db_table = "custom_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
    
