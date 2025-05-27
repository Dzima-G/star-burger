from django.contrib import admin

from places.models import Place


@admin.register(Place)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        'address',
    ]
    list_display = [
        'address',
        'lat',
        'lng',
        'request_data',
    ]


