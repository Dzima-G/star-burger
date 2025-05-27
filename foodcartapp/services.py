from geopy import distance

from .models import Restaurant, RestaurantMenuItem


def get_restaurants_for_order(order):
    order_products = set(order.items.values_list('product__id', flat=True))
    required_count = len(order_products)

    menu_items = RestaurantMenuItem.objects.filter(
        availability=True,
        product_id__in=order_products
    )
    restaurant_product_counts = {}
    for item in menu_items:
        restaurant_product_counts.setdefault(item.restaurant_id, set()).add(item.product_id)

    valid_ids = []
    for rid, prods in restaurant_product_counts.items():
        if len(prods) == required_count:
            valid_ids.append(rid)

    return Restaurant.objects.filter(id__in=valid_ids)


def get_delivery_distance(delivery_coords, restaurant_coords):
    lng1, lat1 = map(float, delivery_coords)
    lng2, lat2 = map(float, restaurant_coords)

    delivery_point = (lat1, lng1)
    restaurant_point = (lat2, lng2)

    distance_km = distance.distance(delivery_point, restaurant_point).km

    return round(distance_km, 2)
