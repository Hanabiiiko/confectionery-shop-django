from django.core.management.base import BaseCommand

from shop.models import Category, Product

CATEGORIES = [
    {'name': 'Торты',             'slug': 'torty'},
    {'name': 'Пирожные',          'slug': 'pirozhnye'},
    {'name': 'Конфеты',           'slug': 'konfety'},
    {'name': 'Печенье',           'slug': 'pechenie'},
    {'name': 'Подарочные наборы', 'slug': 'podarochnye-nabory'},
]

PRODUCTS = [
    # Торты
    {'category': 'torty', 'slug': 'medovik',         'name': 'Медовик классический',        'description': 'Нежные медовые коржи с кремом из сметаны.',             'price': '1200.00', 'weight_grams': 1200},
    {'category': 'torty', 'slug': 'praga',            'name': 'Прага шоколадная',            'description': 'Бисквитный торт с шоколадным кремом и глазурью.',       'price': '1350.00', 'weight_grams': 1100},
    {'category': 'torty', 'slug': 'napoleon',         'name': 'Наполеон слоёный',            'description': 'Хрустящие слои с нежным заварным кремом.',              'price': '1450.00', 'weight_grams': 1300},
    {'category': 'torty', 'slug': 'krasnyj-barkhat',  'name': 'Красный бархат',              'description': 'Бархатистый бисквит с крем-чизом.',                     'price': '1800.00', 'weight_grams': 1500},
    {'category': 'torty', 'slug': 'esterhazi',        'name': 'Эстерхази миндальный',        'description': 'Классика венской кухни: безе, миндаль, пралине.',        'price': '1650.00', 'weight_grams': 1000},

    # Пирожные
    {'category': 'pirozhnye', 'slug': 'ekler',        'name': 'Эклер шоколадный',            'description': 'Заварное тесто с шоколадным кремом.',                   'price': '120.00',  'weight_grams': 80},
    {'category': 'pirozhnye', 'slug': 'makaron',      'name': 'Макарон ванильный',           'description': 'Воздушные миндальные печенья с ванильной начинкой.',    'price': '90.00',   'weight_grams': 30},
    {'category': 'pirozhnye', 'slug': 'kartoshka',    'name': 'Картошка кокосовая',          'description': 'Бисквитные шарики с кокосовой стружкой.',               'price': '85.00',   'weight_grams': 100},
    {'category': 'pirozhnye', 'slug': 'tiramisu',     'name': 'Тирамису порционное',         'description': 'Нежный итальянский десерт с маскарпоне.',                'price': '180.00',  'weight_grams': 150},
    {'category': 'pirozhnye', 'slug': 'ptichye-p',    'name': 'Птичье молоко',               'description': 'Суфле на агаре в шоколадной глазури.',                  'price': '95.00',   'weight_grams': 120},

    # Конфеты
    {'category': 'konfety', 'slug': 'tryufel',        'name': 'Трюфели шоколадные (12 шт)',  'description': 'Ручной работы из бельгийского шоколада.',               'price': '450.00',  'weight_grams': 200},
    {'category': 'konfety', 'slug': 'ptichye-k',      'name': 'Птичье молоко в шоколаде',   'description': 'Нежное суфле в тёмной шоколадной глазури.',             'price': '380.00',  'weight_grams': 250},
    {'category': 'konfety', 'slug': 'griljazh',       'name': 'Грильяж миндальный',          'description': 'Карамелизированный миндаль в шоколаде.',                'price': '290.00',  'weight_grams': 150},
    {'category': 'konfety', 'slug': 'marcipan',       'name': 'Марципановые конфеты',        'description': 'Конфеты из натурального миндального марципана.',        'price': '520.00',  'weight_grams': 180},

    # Печенье
    {'category': 'pechenie', 'slug': 'imbirnoe',      'name': 'Имбирное с глазурью',         'description': 'Пряное имбирное печенье с сахарной глазурью.',          'price': '220.00',  'weight_grams': 300},
    {'category': 'pechenie', 'slug': 'ovsjanoe',      'name': 'Овсяное с изюмом',            'description': 'Домашнее овсяное печенье на сливочном масле.',          'price': '180.00',  'weight_grams': 400},
    {'category': 'pechenie', 'slug': 'biskotti',      'name': 'Миндальное бискотти',         'description': 'Хрустящее итальянское печенье с миндалём.',             'price': '260.00',  'weight_grams': 250},
    {'category': 'pechenie', 'slug': 'rogaliki',      'name': 'Ванильные рогалики',          'description': 'Рассыпчатые рогалики с ванилью и сахарной пудрой.',     'price': '200.00',  'weight_grams': 350},

    # Подарочные наборы
    {'category': 'podarochnye-nabory', 'slug': 'nabor-klassika', 'name': 'Набор «Классика»',    'description': 'Ассорти конфет и печенья в фирменной коробке.',       'price': '890.00',  'weight_grams': 600},
    {'category': 'podarochnye-nabory', 'slug': 'nabor-prazdnik', 'name': 'Набор «Праздничный»', 'description': 'Медовик и 12 трюфелей — идеально для торжества.',    'price': '2200.00', 'weight_grams': 1800},
    {'category': 'podarochnye-nabory', 'slug': 'nabor-detskij',  'name': 'Набор «Детский»',     'description': 'Имбирное печенье и мармелад в ярком оформлении.',     'price': '650.00',  'weight_grams': 500},
    {'category': 'podarochnye-nabory', 'slug': 'nabor-ljuks',    'name': 'Набор «Люкс»',        'description': 'Премиальные шоколадные трюфели в бархатной коробке.', 'price': '1500.00', 'weight_grams': 400},
]


class Command(BaseCommand):
    help = 'Наполняет базу тестовыми данными каталога'

    def handle(self, *args, **kwargs):
        cat_created = 0
        prod_created = 0

        category_map = {}
        for data in CATEGORIES:
            obj, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults={'name': data['name']},
            )
            category_map[data['slug']] = obj
            if created:
                cat_created += 1

        for data in PRODUCTS:
            category = category_map[data['category']]
            _, created = Product.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'category': category,
                    'name': data['name'],
                    'description': data['description'],
                    'price': data['price'],
                    'weight_grams': data['weight_grams'],
                    'image': '',
                    'available': True,
                },
            )
            if created:
                prod_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Готово: создано категорий — {cat_created}, товаров — {prod_created}.'
            )
        )
        self.stdout.write(
            f'Всего в базе: категорий — {Category.objects.count()}, товаров — {Product.objects.count()}.'
        )
