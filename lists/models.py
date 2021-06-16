from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(blank=False, default="")
    list = models.ForeignKey(List, default=None)
