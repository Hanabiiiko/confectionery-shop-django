from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='Slug', unique=True, max_length=200)
    image = models.ImageField(verbose_name='Изображение', upload_to='categories/', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/{self.slug}/'


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='products',
    )
    name = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='Slug', unique=True, max_length=200)
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    weight_grams = models.PositiveIntegerField(verbose_name='Вес (г)', null=True, blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='products/')
    available = models.BooleanField(verbose_name='В наличии', default=True)
    created_at = models.DateTimeField(verbose_name='Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/product/{self.slug}/'


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        choices=[(i, str(i)) for i in range(1, 6)],
    )
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(verbose_name='Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_at',)
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user} → {self.product} ({self.rating}★)'


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Товар',
        on_delete=models.CASCADE,
        related_name='favorited_by',
    )
    created_at = models.DateTimeField(verbose_name='Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} → {self.product}'
