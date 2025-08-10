from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.CharField(
        'адрес',
        unique=True,
        max_length=100,
        blank=True
    )
    lat = models.FloatField(
        verbose_name='Широта',
        null=True,
        blank=True
    )
    lng = models.FloatField(
        verbose_name='Долгота',
        null=True,
        blank=True
    )
    request_data = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата получения геоданных',
        db_index=True
    )

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address
