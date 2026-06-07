from django.conf import settings
from django.db import models


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьер'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('done', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
    )
    full_name = models.CharField('ФИО', max_length=200)
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес', blank=True)
    delivery_method = models.CharField(
        'Способ доставки',
        max_length=10,
        choices=DELIVERY_CHOICES,
        default='pickup',
    )
    delivery_cost = models.DecimalField('Стоимость доставки', max_digits=8, decimal_places=2, default=0)
    promo_code = models.CharField('Промокод', max_length=50, blank=True)
    discount = models.DecimalField('Скидка', max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField('Итого', max_digits=10, decimal_places=2)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )
    is_paid = models.BooleanField('Оплачен', default=False)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk} — {self.full_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.product.name} × {self.quantity}'

    def get_total(self):
        return self.price * self.quantity


class PromoCode(models.Model):
    code = models.CharField('Код', max_length=50, unique=True)
    discount_percent = models.PositiveSmallIntegerField('Скидка (%)')
    active = models.BooleanField('Активен', default=True)
    valid_until = models.DateField('Действует до', null=True, blank=True)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code
