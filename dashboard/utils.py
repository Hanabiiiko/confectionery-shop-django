from django.utils.text import slugify

TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def translit_slug(value):
    text = ''.join(TRANSLIT.get(ch, ch) for ch in value.lower())
    return slugify(text)


def unique_slug(model, name, pk=None):
    base = translit_slug(name) or 'item'
    slug = base
    n = 1
    qs = model.objects.exclude(pk=pk)
    while qs.filter(slug=slug).exists():
        slug = f'{base}-{n}'
        n += 1
    return slug
