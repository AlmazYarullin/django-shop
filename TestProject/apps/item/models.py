from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    price = models.IntegerField()
