# Laboratorio S06 — Motor de plantillas con Django

Portal de noticias en Django que demuestra el motor de plantillas con herencia, fragmentos reutilizables, variables, etiquetas de control, filtros y gestión de contenido desde el administrador. Continúa el proyecto de la semana anterior.

## 1. Descripción

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

## 3. Modelos y relaciones

- **Article** — `title`, `slug`, `content`, `featured_image` (ImageField), `published_at`, `created_at`, `updated_at`
- **Category** — `Article.categories` (N:M): un artículo pertenece a varias categorías
- **Author** — `Article.author` (FK, `CASCADE`): si se borra el autor, se borran sus artículos

## 4. Administrador

- **Category**: `list_display` (name, slug), `prepopulated_fields` (slug desde name), `search_fields`
- **Author**: `list_display` (name, email), `search_fields`
- **Article**: `list_display` (title, author, published_at, categorías), `list_filter` (categories, author, published_at), `search_fields` (title, content), `prepopulated_fields` (slug desde title), `date_hierarchy`, `filter_horizontal` (categories)

## 5. Vistas y URLs

| Vista | URL | Nombre | Template |
|-------|-----|--------|----------|
| `home` | `/` | `news:home` | `news/home.html` |
| `article_detail` | `/articulo/<slug>/` | `news:article_detail` | `news/article_detail.html` |
| `category_list` | `/categoria/<slug>/` | `news:category_list` | `news/category_list.html` |

Todas las URLs usan `{% url 'news:nombre' %}` en plantillas.

## 6. Estructura de plantillas

```
templates/
├── base.html                    # Plantilla base con bloques title, content, sidebar
└── news/
    ├── _article_card.html       # Fragmento reutilizable (tarjeta de artículo)
    ├── _article_cover.html      # Portada individual, con prioridad para imágenes del admin
    ├── _icon_home.html          # Icono SVG home
    ├── _icon_category.html      # Icono SVG categoría
    ├── _icon_admin.html         # Icono SVG admin
    ├── _icon_date.html          # Icono SVG fecha
    ├── _icon_author.html        # Icono SVG autor
    ├── _icon_arrow.html         # Icono SVG flecha
    ├── home.html                # Portada (extiende base.html)
    ├── article_detail.html      # Detalle de noticia (extiende base.html)
    └── category_list.html       # Listado por categoría (extiende base.html)
```

**Herencia y reutilización**:
- `base.html` define estructura común y bloques
- `home.html`, `article_detail.html`, `category_list.html` extienden `base.html`
- `_article_card.html` se incluye en `home.html` y `category_list.html` (sin duplicar marcado)
- Iconos SVG en `templates/news/_icon_*.html`, incluidos con `{% include %}`

## 7. Estáticos y medios

```
static/
├── css/
│   └── style.css           # Variables CSS, responsive, animaciones, iconos SVG
├── img/
│   ├── logo.svg            # Logotipo con gradiente
│   └── news-decor.svg      # Ilustración decorativa animada (SMIL)
└── js/                     # (vacío)

media/
└── articles/               # Imágenes subidas desde admin (ImageField)
```

- `STATICFILES_DIRS = [BASE_DIR / 'static']`, `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'`
- Servidos en desarrollo desde `config/urls.py` con `static()`

## 8. Diseño visual

- **Variables CSS** (`:root`): colores, espaciados, tipografía, bordes, transiciones
- **Responsive**: Grid (layout principal y noticias), Flexbox (nav y tarjetas), breakpoints 900px y 620px
- **Iconos SVG inline**: 6 fragmentos propios, trazo fino y consistente, `aria-hidden="true"` (decorativos)
- **Animaciones**: entrada escalonada de tarjetas, pulso decorativo y efectos hover; `prefers-reduced-motion: reduce` desactiva el movimiento
- **Ilustración decorativa**: `static/img/news-decor.svg` con animaciones SMIL
- **Portadas**: foto de Unsplash propia para cada noticia de ejemplo; las imágenes subidas desde Administración tienen prioridad y las noticias nuevas reciben una portada estable según su slug. El mismo fallback se usa en listados y detalle.
- **Accesibilidad**: enlace para saltar al contenido y foco visible en la navegación por teclado

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

## 11. Datos de prueba

Comando `populate_news` crea:
- 3 categorías: Tecnología, Deportes, Cultura (con descripciones)
- 3 autores: Ana García, Carlos López, María Rodríguez
- 6 artículos (2 por categoría) con fechas escalonadas

## 12. Pruebas y casos de aceptación

```bash
# Verificación de configuración
python manage.py check

# Pruebas automatizadas
python manage.py test

# Prueba escapado automático (manual)
# 1. Crear artículo con HTML: <script>alert("XSS")</script><b>negrita</b>
# 2. Ver en /articulo/<slug>/ → HTML mostrado como texto, no ejecutado
```

| Caso | Descripción | Resultado esperado |
|------|-------------|-------------------|
| Portada con noticias | Artículos publicados | Una tarjeta por artículo, con portada, título, fecha, autor y extracto |
| Portada sin noticias | BD sin artículos | Mensaje "No hay noticias publicadas aún" |
| Detalle noticia | Acceso a `/articulo/<slug>/` | Portada, título, fecha, autor, contenido y categorías |
| Categoría vacía | `/categoria/<slug>/` sin artículos | Mensaje "No hay noticias en esta categoría" |
| Categoría con noticias | Categoría con artículos | Tarjetas reutilizando `_article_card.html` |
| Enlaces `{% url %}` | Navegación, sidebar y tarjetas | URLs correctas, sin rutas hardcodeadas |
| Estáticos CSS/IMG | CSS, imágenes e iconos | Recursos disponibles y renderizados |
| Admin CRUD | Crear/editar/borrar en `/admin/` | Cambios reflejados en el portal sin tocar código |
| Escapado XSS | Artículo con `<script>` | HTML escapado; el script no se ejecuta |
| Responsive | Ventanas de 900 px y 620 px | Layout y navegación adaptados al ancho disponible |

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
│       ├── _article_cover.html
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

---

**Autor**: [Nombre del alumno]
**Curso**: Desarrollo de Aplicaciones Empresariales, 4-C24-A
**Semana**: S06 - Motor de plantillas con Django
