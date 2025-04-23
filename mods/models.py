from django.db import models
from django.conf import settings

class Mod(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    game = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mods')
    upload_date = models.DateTimeField(auto_now_add=True)
    # Placeholder for versioning, categories, tags, etc.

    def __str__(self):
        return self.title
