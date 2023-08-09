from django.db import models


class DeltaLink(models.Model):
    link = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
