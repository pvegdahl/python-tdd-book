from django.db import models
from django.urls import reverse

from superlists import settings


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self) -> str:
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    text = models.TextField(blank=False, default="")
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")

    def __str__(self):
        return self.text
