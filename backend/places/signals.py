from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Place
from .utils import fetch_coordinates


@receiver(post_save, sender='foodcartapp.Restaurant')
def create_place_for_restaurant(sender, instance, created, **kwargs):
    address = instance.address
    if not address:
        return

    place, was_created = Place.objects.get_or_create(
        address=address,
        defaults={'lat': None, 'lng': None}
    )
    if was_created:
        coords = fetch_coordinates(address)
        if coords:
            place.lat, place.lng = coords
            place.save()


@receiver(post_save, sender='foodcartapp.Order')
def create_place_for_order(sender, instance, created, **kwargs):
    address = instance.delivery_address
    if not address:
        return
    place, was_created = Place.objects.get_or_create(
        address=address,
        defaults={'lat': None, 'lng': None}
    )
    if was_created:
        coords = fetch_coordinates(address)
        if coords:
            place.lat, place.lng = coords
            place.save()
