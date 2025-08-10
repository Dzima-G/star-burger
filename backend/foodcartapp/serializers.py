from rest_framework.serializers import CharField, ModelSerializer

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    address = CharField(source='delivery_address')
    products = OrderItemSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']


    def create(self, validated_data):
        products_data = validated_data.pop('products')

        order = Order.objects.create(**validated_data)

        order_items = []
        for item in products_data:
            product = item['product']
            quantity = item['quantity']
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
            )

        OrderItem.objects.bulk_create(order_items)

        return order
