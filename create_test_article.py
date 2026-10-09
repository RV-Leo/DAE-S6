from news.models import Article, Category, Author
from django.utils import timezone

# Get or create a test category and author
cat, _ = Category.objects.get_or_create(name='Prueba', slug='prueba')
author, _ = Author.objects.get_or_create(email='test@example.com', defaults={'name': 'Test User'})

# Create article with HTML content
article = Article.objects.create(
    title='Prueba de escapado HTML',
    slug='prueba-escapado-html',
    content='<script>alert("XSS")</script><b>Texto en negrita</b><i>Texto en cursiva</i>',
    published_at=timezone.now(),
    author=author
)
article.categories.add(cat)
print(f'Creado: {article.title} (slug: {article.slug})')