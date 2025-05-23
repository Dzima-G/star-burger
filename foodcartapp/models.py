from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import DecimalField, F, Sum
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=500,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrdersQuerySet(models.QuerySet):
    def with_total_price(self):
        return self.annotate(
            total_price=Sum(
                F('items__price') * F('items__quantity'),
                output_field=DecimalField()
            )
        )


class Order(models.Model):
    STATUS_CHOICES = [
        ('unprocessed', 'Необработанный'),
        ('underway', 'В работе'),
        ('delivery', 'Доставка'),
        ('completed', 'Завершен'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Наличный'),
        ('non_cash', 'Безналичный')
    ]

    firstname = models.CharField(
        max_length=50,
        verbose_name='Имя',
        null=False
    )
    lastname = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        null=False
    )
    phonenumber = PhoneNumberField(
        region='RU',
        verbose_name='Мобильный телефон',
        db_index=True
    )
    delivery_address = models.CharField(
        max_length=300,
        verbose_name='Адрес доставки',
        null=False
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unprocessed',
        db_index=True,
        verbose_name='Статус'
    )
    comment = models.TextField(
        verbose_name='Коментарий',
        blank=True
    )
    registered_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Зарегистрирован',
        db_index=True
    )
    called_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Прозвонен',
        db_index=True
    )
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Доставлен',
        db_index=True
    )
    payment = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash',
        db_index=True,
        verbose_name='Способ оплаты'
    )

    objects = OrdersQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.id}. {self.firstname} {self.lastname}; {self.delivery_address}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        null=False
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True
    )

    class Meta:
        verbose_name = 'Заказанные товары'
        verbose_name_plural = 'Заказанные товары'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
