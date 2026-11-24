import os
from datetime import date
import django
from django.utils import timezone
from PIL import Image, ImageDraw

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab08.settings')
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from series.models import Serie
from tienda.models import Categoria, Producto


def ensure_superuser():
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@tecsup.edu.pe', 'is_staff': True, 'is_superuser': True},
    )
    user.is_staff = True
    user.is_superuser = True
    user.email = 'admin@tecsup.edu.pe'
    user.set_password('Tecsup2023')
    user.save()
    print(f"Superusuario 'admin' {'creado' if created else 'verificado'} (clave: Tecsup2023).")


def seed_series_iniciales():
    """Inserta los 3 registros iniciales indicados en la guía del Lab 08."""
    series_iniciales = [
        {
            'name': 'Breaking Bad',
            'release_date': date(2008, 1, 20),
            'rating': 5,
            'category': Serie.DRAMA,
        },
        {
            'name': 'The Office',
            'release_date': date(2005, 3, 24),
            'rating': 5,
            'category': Serie.COMEDY,
        },
        {
            'name': 'Stranger Things',
            'release_date': date(2016, 7, 15),
            'rating': 4,
            'category': Serie.HORROR,
        },
    ]
    for item in series_iniciales:
        obj, created = Serie.objects.get_or_create(
            name=item['name'],
            defaults={
                'release_date': item['release_date'],
                'rating': item['rating'],
                'category': item['category'],
            },
        )
        print(f"Serie inicial {'creada' if created else 'existente'}: {obj.id} - {obj.name}")


def generate_banner(title, subtitle, bg_color, text_color=(255, 255, 255), width=600, height=400):
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([12, 12, width - 12, height - 12], outline=(255, 255, 255), width=3)
    draw.ellipse(
        [width // 2 - 90, height // 2 - 120, width // 2 + 90, height // 2 + 60],
        outline=(255, 255, 255),
        width=2,
    )
    draw.text((width // 2, height // 2 - 40), title, fill=text_color, anchor='mm')
    draw.text((width // 2, height // 2 + 10), subtitle, fill=text_color, anchor='mm')
    draw.text((width // 2, height - 40), 'Tecsup WebShop API', fill=(240, 240, 240), anchor='mm')
    return img


def seed_tienda():
    """Carga las 4 categorías y 10 productos del Laboratorio 06."""
    media_cat = os.path.join(settings.MEDIA_ROOT, 'categorias')
    media_prod = os.path.join(settings.MEDIA_ROOT, 'productos')
    os.makedirs(media_cat, exist_ok=True)
    os.makedirs(media_prod, exist_ok=True)

    cat_data = {
        'Gaseosas': (231, 76, 60),
        'Snacks': (243, 156, 18),
        'Galletas': (142, 68, 173),
        'Chocolates': (108, 52, 131),
    }

    cat_objs = {}
    for cat_name, color in cat_data.items():
        cat, created = Categoria.objects.get_or_create(nombre=cat_name)
        if not cat.imagen:
            cat_img_path = os.path.join(media_cat, f'{cat_name.lower()}.png')
            img = generate_banner(cat_name.upper(), 'Categoría Oficial', color, width=400, height=400)
            img.save(cat_img_path)
            with open(cat_img_path, 'rb') as f:
                cat.imagen.save(f'{cat_name.lower()}.png', File(f), save=False)
            cat.save()
        cat_objs[cat_name] = cat
        print(f"Categoría {'creada' if created else 'existente'}: {cat.id} - {cat.nombre}")

    productos_data = [
        ('Gaseosas', 'Fanta 500ml', 1.80, 10, (230, 126, 34), 'Gaseosa sabor a naranja 500ml bien helada.'),
        ('Gaseosas', 'Coca Cola 500ml', 2.50, 10, (192, 57, 43), 'El sabor original y refrescante de Coca Cola 500ml.'),
        ('Gaseosas', '7up 500ml', 1.70, 10, (39, 174, 96), 'Gaseosa lima-limón 500ml sin cafeína.'),
        ('Snacks', 'Cheetos', 1.00, 12, (211, 84, 0), 'Snack horneado sabor a queso crunch.'),
        ('Snacks', 'Chizito', 1.00, 12, (241, 196, 15), 'Clásico chizito sabor a queso peruano.'),
        ('Galletas', 'Picaras', 1.00, 12, (125, 60, 152), 'Galletas bañadas con exquisita cobertura de chocolate.'),
        ('Galletas', 'Coronita Fresa', 0.70, 12, (233, 30, 99), 'Galleta rellena con deliciosa crema sabor a fresa.'),
        ('Chocolates', 'Princesa', 1.50, 8, (155, 89, 182), 'Bombón relleno con deliciosa crema de maní y chocolate.'),
        ('Chocolates', 'Sublime', 1.50, 8, (41, 128, 185), 'Chocolate con leche y trozos de maní tostado.'),
        ('Chocolates', 'Triángulo', 1.20, 8, (243, 156, 18), 'Chocolate clásico en forma triangular.'),
    ]

    for cat_name, prod_name, precio, stock, color, desc in productos_data:
        cat = cat_objs[cat_name]
        prod, created = Producto.objects.get_or_create(
            nombre=prod_name,
            defaults={
                'categoria': cat,
                'precio': precio,
                'stock': stock,
                'descripcion': desc,
                'pub_date': timezone.now(),
            },
        )
        if not prod.imagen:
            filename = prod_name.lower().replace(' ', '_') + '.png'
            prod_img_path = os.path.join(media_prod, filename)
            img = generate_banner(prod_name, f'S/ {precio:.2f} | Stock: {stock}', color)
            img.save(prod_img_path)
            with open(prod_img_path, 'rb') as f:
                prod.imagen.save(filename, File(f), save=False)
            prod.save()
        print(f"Producto {'creado' if created else 'existente'}: {prod.id} - {prod.nombre}")


if __name__ == '__main__':
    ensure_superuser()
    seed_series_iniciales()
    seed_tienda()
    print("\n¡Datos iniciales sembrados correctamente!")
