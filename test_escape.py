import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from news.models import Article, Category, Author
from django.utils import timezone

cat, _ = Category.objects.get_or_create(name='Prueba', slug='prueba')
author, _ = Author.objects.get_or_create(email='test@example.com', defaults={'name': 'Test User'})

html_content = '<script>alert("XSS")</script><b>Texto en negrita</b><i>Texto en cursiva</i>'

article = Article.objects.create(
    title='Prueba de escapado HTML',
    slug='prueba-escapado-html',
    content=html_content,
    published_at=timezone.now(),
    author=author
)
article.categories.add(cat)
print(f'Creado: {article.title}')