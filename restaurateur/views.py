from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from foodcartapp.models import Order, Product, Restaurant
from foodcartapp.services import (get_delivery_distance,
                                  get_restaurants_for_order)
from places.models import Place


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    qs = Order.objects.with_total_price().exclude(status='completed')
    orders = list(qs)
    priority = {
        'unprocessed': 1,
        'underway': 2,
        'delivery': 3,
    }
    orders.sort(key=lambda o: priority.get(o.status, 5))

    for order in orders:
        order.coords_error = False

        restaurants = get_restaurants_for_order(order)

        order_place = Place.objects.filter(address=order.delivery_address).first()

        if not order_place or order_place.lat is None or order_place.lng is None:
            order.coords_error = True
            order.available_restaurants = []
            continue
        delivery_coords = (order_place.lng, order_place.lat)

        if delivery_coords[0] is None or delivery_coords[1] is None:
            order.coords_error = True
            order.available_restaurants = []
            continue

        for rest in restaurants:
            restaurant_place = Place.objects.filter(address=rest.address).first()
            if restaurant_place:
                restaurant_coords = (restaurant_place.lng, restaurant_place.lat)
            else:
                order.coords_error = True
                break

            rest.distance = get_delivery_distance(delivery_coords, restaurant_coords)

        if order.coords_error:
            order.available_restaurants = []
        else:
            order.available_restaurants = restaurants

    return render(request, 'order_items.html', {
        'order_items': orders,
    })
