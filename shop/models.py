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
