# Laboratorio S06 — Motor de plantillas con Django

Portal de noticias en Django que demuestra el motor de plantillas con herencia, fragmentos reutilizables, variables, etiquetas de control, filtros y gestión de contenido desde el administrador.

## 1. Descripción

Proyecto acumulativo que continúa el trabajo de semanas anteriores. Implementa una aplicación `news` con:

- Plantilla base con herencia (`base.html`) y bloques `title`, `content`, `sidebar`
- Fragmento reutilizable `_article_card.html` incluido con `{% include %}` en portada y listado por categoría
- Portada con `{% for %}`, `{% empty %}` y filtros `date`, `truncatewords`
- Detalle de noticia con imagen, autor, categorías y contenido formateado
- Listado por categoría reutilizando el mismo fragmento
- Panel de administración personalizado para Article, Category, Author
- 6 noticias de prueba en 3 categorías (Tecnología, Deportes, Cultura)
- Diseño responsive con CSS variables, iconos SVG inline, animaciones CSS/SMIL
- Escapado automático HTML (prevención XSS) verificado

## 2. Tecnologías

- Python 3.12+
- Django 5.2+
- Pillow 12.3+ (ImageField)
- SQLite (desarrollo)
- CSS nativo (variables, grid, flexbox, animaciones)
- SVG inline (iconos, logotipo, ilustraciones)

## 3. Estructura de plantillas

```
templates/
├── base.html                    # Plantilla base con herencia
│   Bloques: title, content, sidebar
│   Incluye: _icon_home.html, _icon_admin.html (en nav)
└── news/
    ├── _article_card.html       # Fragmento reutilizable (tarjeta de artículo)
    │   Incluye: _icon_date.html, _icon_author.html, _icon_arrow.html
    ├── _icon_home.html          # Icono SVG home
    ├── _icon_category.html      # Icono SVG categoría
    ├── _icon_admin.html         # Icono SVG admin
    ├── _icon_date.html          # Icono SVG fecha
    ├── _icon_author.html        # Icono SVG autor
    ├── _icon_arrow.html         # Icono SVG flecha
    ├── home.html                # Portada (extiende base.html)
    │   Usa: {% for article in articles %} {% include 'news/_article_card.html' %} {% empty %} {% endfor %}
    ├── article_detail.html      # Detalle de noticia (extiende base.html)
    │   Muestra: imagen, título, fecha, autor, contenido (linebreaks), categorías con enlaces
    └── category_list.html       # Listado por categoría (extiende base.html)
        Usa: {% for article in articles %} {% include 'news/_article_card.html' %} {% empty %} {% endfor %}
```

### Herencia y reutilización

| Plantilla | Extiende | Incluye fragmentos | Bloques usados |
|-----------|----------|-------------------|----------------|
| `base.html` | — | `_icon_home.html`, `_icon_admin.html` | `title`, `content`, `sidebar` |
| `home.html` | `base.html` | `_article_card.html` (×N) | `title`, `content` |
| `article_detail.html` | `base.html` | `_icon_date.html`, `_icon_author.html` | `title`, `content` |
| `category_list.html` | `base.html` | `_icon_category.html`, `_article_card.html` (×N) | `title`, `content` |
| `_article_card.html` | — | `_icon_date.html`, `_icon_author.html`, `_icon_arrow.html` | — (fragmento) |

**Sin duplicación de marcado**: `_article_card.html` se usa en `home.html` y `category_list.html`.

## 4. Modelos

- **Category**: `name`, `slug`, `description`
- **Author**: `name`, `email`, `bio`
- **Article**: `title`, `slug`, `content`, `featured_image` (ImageField), `published_at`, `author` (FK), `categories` (M2M), `created_at`, `updated_at`

## 5. Vistas y URLs

| Vista | URL | Nombre | Template |
|-------|-----|--------|----------|
| `home` | `/` | `news:home` | `news/home.html` |
| `article_detail` | `/articulo/<slug>/` | `news:article_detail` | `news/article_detail.html` |
| `category_list` | `/categoria/<slug>/` | `news:category_list` | `news/category_list.html` |

Todas las URLs usan `{% url 'news:nombre' %}` en plantillas.

## 6. Administrador

Registrados con `list_display`, `list_filter`, `search_fields`, `prepopulated_fields`, `date_hierarchy`, `filter_horizontal`:

- **Category**: nombre, slug, descripción
- **Author**: nombre, email, bio
- **Article**: título, autor, fecha, categorías, imagen, slug auto

Datos de prueba: comando `populate_news` crea 3 categorías, 3 autores, 6 artículos.

## 7. Estáticos y medios

```
static/
├── css/
│   └── style.css           # Variables CSS, responsive, animaciones, SVG
├── img/
│   ├── logo.svg            # Logotipo con gradiente
│   └── news-decor.svg      # Ilustración decorativa animada (SMIL)
└── js/                     # (vacío, solo si necesario)

media/
└── articles/               # Imágenes subidas desde admin (ImageField)
```

- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'`
- Servidos en desarrollo desde `config/urls.py` con `static()`

## 8. Diseño visual

- **Variables CSS** (`:root`): colores, espaciados, tipografía, bordes, transiciones
- **Responsive**: Grid (layout principal), Flexbox (nav, tarjetas), breakpoints 768px
- **Iconos SVG inline**: 6 fragmentos en `templates/news/_icon_*.html`, incluidos con `{% include %}`, `aria-hidden="true"` (decorativos)
- **Animaciones**: `fadeInUp` en tarjetas (staggered delays), `prefers-reduced-motion: reduce` desactiva CSS y SMIL
- **Ilustración decorativa**: `static/img/news-decor.svg` con animaciones SMIL

## 9. Seguridad

- `SECRET_KEY` en `.env` (no en código)
- `DEBUG = True` solo desarrollo
- Escapado automático: `{{ variable }}` escapa HTML por defecto
- Sin `|safe` ni `{% autoescape off %}` en producción
- Prueba verificada: artículo con `<script>alert("XSS")</script>` se muestra como texto plano
- `.gitignore` incluye: `venv/`, `__pycache__/`, `db.sqlite3`, `.env`, `media/`, `staticfiles/`

## 10. Instalación y ejecución

```bash
# Clonar repositorio
git clone <url>
cd DAE-S6

# Entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Dependencias
pip install -r requirements.txt

# Variables de entorno
copy .env.example .env
# Editar .env con DJANGO_SECRET_KEY

# Base de datos
python manage.py migrate

# Superusuario
python manage.py createsuperuser

# Datos de prueba (opcional)
python manage.py populate_news

# Estáticos
python manage.py collectstatic --noinput

# Servidor
python manage.py runserver
```

- Admin: http://127.0.0.1:8000/admin/
- Portal: http://127.0.0.1:8000/

## 11. Tests y verificación

```bash
# Verificación de configuración
python manage.py check

# Tests
python manage.py test

# Prueba escapado automático
# 1. Crear artículo con HTML: <script>alert("XSS")</script><b>negrita</b>
# 2. Ver en /articulo/<slug>/ → HTML mostrado como texto, no ejecutado
```

## 12. Casos de prueba

| Caso | Descripción | Resultado esperado |
|------|-------------|-------------------|
| Portada con noticias | 6 artículos publicados | 6 tarjetas con imagen, título, fecha, autor, extracto |
| Portada sin noticias | BD vacía | Mensaje "No hay noticias publicadas aún" |
| Detalle noticia | Acceso a `/articulo/<slug>/` | Imagen, título, fecha, autor, contenido, categorías |
| Categoría vacía | `/categoria/<slug>/` sin artículos | Mensaje "No hay noticias en esta categoría" |
| Categoría con noticias | 2 artículos por categoría | 2 tarjetas usando `_article_card.html` |
| Enlaces `{% url %}` | Navegación header, sidebar, tarjetas | URLs correctas, sin hardcoded |
| Estáticos CSS/IMG | Carga de style.css, logo.svg, iconos | 200 OK, estilos aplicados, SVG renderizados |
| Admin CRUD | Crear/editar/borrar en /admin/ | Cambios reflejados en portal sin tocar código |
| Escapado XSS | Artículo con `<script>` | HTML escapado, no ejecutado |
| Responsive | < 768px | Sidebar apilado, navegación usable |

## 13. Estructura del proyecto

```
DAE-S6/
├── manage.py
├── requirements.txt
├── README.md
├── PROGRESS.md
├── .gitignore
├── .env.example
├── .env                    # (no versionado)
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/
│   ├── __init__.py
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── populate_news.py
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_initial.py
│       └── 0002_category_description.py
├── templates/
│   ├── base.html
│   └── news/
│       ├── _article_card.html
│       ├── _icon_home.html
│       ├── _icon_category.html
│       ├── _icon_admin.html
│       ├── _icon_date.html
│       ├── _icon_author.html
│       ├── _icon_arrow.html
│       ├── home.html
│       ├── article_detail.html
│       └── category_list.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── img/
│   │   ├── logo.svg
│   │   └── news-decor.svg
│   └── js/
└── media/
    └── articles/           # (creado al subir imágenes)
```

