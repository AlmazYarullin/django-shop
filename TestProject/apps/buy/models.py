import stripe
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from TestProject.apps.item.models import Item


class Tax(models.Model):
    tax_rate_id = models.CharField(max_length=30, blank=True)
    name = models.TextField()
    percentage = models.FloatField(max_length=100)
    inclusive = models.BooleanField()
    country = models.TextField()

    def __str__(self):
        return f"{self.name} | {self.percentage}%"

    def clean(self):
        self.clean_fields()
        try:
            self.tax_rate_id = stripe.TaxRate.create(
                display_name=self.name,
                inclusive=self.inclusive,
                percentage=self.percentage,
                country=self.country,
            )['id']
        except Exception as e:
            raise ValidationError(e)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Discount(models.Model):
    percentage = models.FloatField(max_length=100)
    discount_id = models.TextField(blank=True)

    def __str__(self):
        return f"{self.percentage}%"

    def clean(self):
        self.clean_fields()
        try:
            self.discount_id = stripe.Coupon.create(percent_off=self.percentage)['id']
        except Exception as e:
            raise ValidationError(e)


class Order(models.Model):
    created_at = models.DateTimeField(default=now)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, default=None, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.created_at}"


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
