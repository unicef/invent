from django.db import models


class DeltaLink(models.Model):
    url = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_latest_link(cls):
        return cls.objects.order_by("-created").first()
