from django.http import JsonResponse
from django.templatetags.static import static
from phonenumbers import NumberParseException, parse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, OrderItem, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    try:
        data = request.data
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        phone_number = data.get('phonenumber')
        delivery_address = data.get('address')
        products_data = data.get('products')

        missing_fields = []

        if not firstname:
            missing_fields.append('firstname')
        if not lastname:
            missing_fields.append('lastname')
        if not phone_number:
            missing_fields.append('phonenumber')
        if not delivery_address:
            missing_fields.append('address')
        if not products_data:
            missing_fields.append('products')

        if missing_fields:
            return Response({'error': f'This field cannot be empty {missing_fields}.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            phone_number = parse(phone_number, 'RU')
        except NumberParseException:
            return Response({'error': f'Incorrect phone number {phone_number}.'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(products_data, list):
            return Response({'error': f'Expected a list of values but got {type(products_data)}.'},
                            status=status.HTTP_400_BAD_REQUEST)

        for product_data in products_data:
            product_id = product_data.get('product')
            quantity = product_data.get('quantity')

            if not product_id or not quantity:
                return Response({'error': f'No data available'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product_id = int(product_id)
                quantity = int(quantity)
            except ValueError:
                return Response({'error': f'Invalid data type {product_id} or {quantity}'},
                                status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            firstname=data.get('firstname'),
            lastname=data.get('lastname'),
            phone_number=parse(data.get('phonenumber'), 'RU'),
            delivery_address=data.get('address')
        )

        for product_data in data.get('products'):
            product_id = int(product_data['product'])
            quantity = int(product_data['quantity'])
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

    except Exception as e:
        return Response({'error': f'Data processing error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({})
