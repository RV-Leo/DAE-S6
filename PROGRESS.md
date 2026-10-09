# Avance del laboratorio S06

## Completado

- Paso 0: Abrir VS Code con `code .` y esperar confirmación
- Paso 1: Se continuó el proyecto de la Semana 5, se creó el entorno virtual con Python 3.12, se instalaron Django y Pillow, y se creó y registró la aplicación `news`.
- Paso 2: Configurar directorio de plantillas, estáticos y medios; servir medios desde `config/urls.py`.
- Paso 3: Modelos `Article`, `Category`, `Author`; migraciones aplicadas; superusuario creado.
- Paso 4: `base.html` con bloques `title`, `content`, `sidebar` y hoja de estilos CSS.
- Paso 5: Fragmento `_article_card.html` incluido en portada (`home.html`) con `{% for %}` y `{% empty %}`.
- Paso 6: Portada con `for`, `empty` y filtros `date`, `truncatewords` (implementado en Paso 5).
- Paso 7: Detalle de noticia (`article_detail.html`) con imagen, autor, categorías, heredando de `base.html`.
- Paso 8: Listado por categoría (`category_list.html`) reutilizando `_article_card.html`.
- Paso 9: Rutas con nombre (`news:home`, `news:article_detail`, `news:category_list`) y enlaces con `{% url %}`; context processor para categorías en sidebar.
- Paso 10: `{% load static %}`, comprobación CSS/imágenes, diseño con CSS variables, SVG inline (iconos, logo, ilustración), animaciones CSS/SMIL, `prefers-reduced-motion`.
- Paso 11: Personalizar admin; 6 noticias en 3 categorías via comando `populate_news`.
- Paso 12: Probar escapado automático — artículo con `<script>alert("XSS")</script>` se muestra como texto plano (Django escapa por defecto).
- Paso 13: Preparar repositorio y entregable — `README.md` con estructura de plantillas explicada, casos de prueba, instrucciones de captura.

## Pendiente

- (Ninguno — todos los pasos completados)

## Próximos pasos para el usuario

1. Ejecutar `python manage.py check` y `python manage.py test`
2. Tomar las 8 capturas indicadas en README.md sección 14
3. Redactar el entregable en español con el formato exigido
4. Subir repositorio a GitHub (commits manuales del usuario)
5. Subir entregable al campus virtual
6. Cerrar sesiones de GitHub y campus virtual