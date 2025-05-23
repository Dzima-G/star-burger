from .models import Restaurant, RestaurantMenuItem


def get_restaurants_for_order(order):
    order_products = order.items.values_list('product__id', flat=True)

    menu_items = RestaurantMenuItem.objects.filter(
        availability=True,
        product_id__in=order_products
    )

    restaurant_product_counts = {}

    for item in menu_items:
        restaurant_id = item.restaurant_id
        restaurant_product_counts.setdefault(restaurant_id, set()).add(item.product_id)

    required_product_count = len(set(order_products))

    valid_restaurant_ids = [
        restaurant_id
        for restaurant_id, product_ids in restaurant_product_counts.items()
        if len(product_ids) == required_product_count
    ]

    return Restaurant.objects.filter(id__in=valid_restaurant_ids)
