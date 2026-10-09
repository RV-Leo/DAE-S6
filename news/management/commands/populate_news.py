from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from news.models import Category, Author, Article


class Command(BaseCommand):
    help = 'Crea 6 noticias de prueba en 3 categorías'

    def handle(self, *args, **options):
        # Crear categorías
        tech, _ = Category.objects.get_or_create(
            name='Tecnología',
            slug='tecnologia',
            defaults={'description': 'Noticias sobre tecnología, ciencia e innovación'}
        )
        sports, _ = Category.objects.get_or_create(
            name='Deportes',
            slug='deportes',
            defaults={'description': 'Resultados, crónicas y actualidad deportiva'}
        )
        culture, _ = Category.objects.get_or_create(
            name='Cultura',
            slug='cultura',
            defaults={'description': 'Arte, cine, música, literatura y eventos culturales'}
        )

        # Crear autores
        author1, _ = Author.objects.get_or_create(
            email='ana.garcia@example.com',
            defaults={'name': 'Ana García', 'bio': 'Periodista especializada en tecnología.'}
        )
        author2, _ = Author.objects.get_or_create(
            email='carlos.lopez@example.com',
            defaults={'name': 'Carlos López', 'bio': 'Redactor deportivo con 10 años de experiencia.'}
        )
        author3, _ = Author.objects.get_or_create(
            email='maria.rodriguez@example.com',
            defaults={'name': 'María Rodríguez', 'bio': 'Crítica cultural y escritora.'}
        )

        # Crear artículos
        articles_data = [
            {
                'title': 'La IA revoluciona la medicina',
                'content': 'La inteligencia artificial está transformando el diagnóstico médico con algoritmos capaces de detectar enfermedades con mayor precisión que los métodos tradicionales. Los hospitales ya implementan estas herramientas para mejorar la atención al paciente.',
                'author': author1,
                'categories': [tech],
                'days_ago': 1,
            },
            {
                'title': 'Nuevo smartphone rompe récords de ventas',
                'content': 'El último modelo de la marca líder ha superado todas las previsiones de venta en su primer fin de semana. Las innovaciones en cámara y batería son los principales atractivos para los consumidores.',
                'author': author1,
                'categories': [tech],
                'days_ago': 3,
            },
            {
                'title': 'El equipo local gana el campeonato',
                'content': 'En una final emocionante decidida en la prórroga, el equipo local se coronó campeón ante su afición. El delantero estrella marcó el gol decisivo en el minuto 112.',
                'author': author2,
                'categories': [sports],
                'days_ago': 2,
            },
            {
                'title': 'Traspaso histórico en el mercado de fichajes',
                'content': 'El traspaso más caro de la historia se ha confirmado oficialmente. El jugador cambiará de liga en una operación que supera los 200 millones de euros.',
                'author': author2,
                'categories': [sports],
                'days_ago': 5,
            },
            {
                'title': 'Festival de cine anuncia su programación',
                'content': 'El prestigioso festival internacional ha desvelado la selección oficial de este año, con películas de 40 países compitiendo por el galardón principal. La inauguración será el próximo mes.',
                'author': author3,
                'categories': [culture],
                'days_ago': 4,
            },
            {
                'title': 'Nueva exposición de arte contemporáneo abre sus puertas',
                'content': 'El museo de arte moderno presenta una retrospectiva del artista emergente más influyente de la década. La muestra incluye instalaciones interactivas y obras nunca antes expuestas.',
                'author': author3,
                'categories': [culture],
                'days_ago': 6,
            },
        ]

        for data in articles_data:
            categories = data.pop('categories')
            days_ago = data.pop('days_ago')
            slug = slugify(data['title'])
            article, created = Article.objects.get_or_create(
                slug=slug,
                defaults={
                    **data,
                    'published_at': timezone.now() - timedelta(days=days_ago),
                }
            )
            if created:
                article.categories.set(categories)
                self.stdout.write(self.style.SUCCESS(f'Creado: {article.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Ya existe: {article.title}'))

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados correctamente.'))