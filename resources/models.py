from collections.abc import Iterable
import datetime
from dateutil import relativedelta
from django.db import models
from django.conf import settings


class Resource(models.Model):
    """This class represents the company's resources, such as T-shirt, trousers etc."""

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration_years = models.IntegerField(
        choices=[(i, i) for i in range(0, 11)], default=0
    )
    duration_months = models.IntegerField(
        choices=[(i, i) for i in range(0, 13)], default=0
    )
    duration_days = models.IntegerField(
        choices=[(i, i) for i in range(0, 32)], default=0
    )

    def __str__(self):
        return self.name


class Employee(models.Model):
    """This class represents the company's employees."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ResourceRelease(models.Model):
    """This class represents the company's resources, such as T-shirt, trousers etc."""

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    released_at = models.DateTimeField(auto_now_add=True, editable=True)
    released_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=True,
    )
    released_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    valid_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.resource} released to {self.released_to}"

    def save(self, *args, **kwargs) -> None:
        duration = relativedelta.relativedelta(
            years=self.resource.duration_years,
            months=self.resource.duration_months,
            days=self.resource.duration_days,
        )
        if not self.released_at:
            self.valid_until = datetime.datetime.now() + duration
        else:
            self.valid_until = self.released_at + duration
        return super().save(*args, **kwargs)
