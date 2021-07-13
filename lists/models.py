from typing import Optional

from django.db import models
from django.urls import reverse

from accounts.models import User
from superlists import settings


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self) -> str:
        return reverse("view_list", args=[self.id])

    @classmethod
    def create_new(cls, first_item_text: str, owner: Optional[User] = None):
        new_list = cls.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=new_list)
        return new_list


class Item(models.Model):
    text = models.TextField(blank=False, default="")
    list = models.ForeignKey(List, default=None)

    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")

    def __str__(self):
        return self.text
