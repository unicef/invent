from django.db import models


class DeltaLink(models.Model):
    url = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_latest_link(cls):
        return cls.objects.order_by('-updated_at').first()
