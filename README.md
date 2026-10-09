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
- **Responsive**: Grid (layout principal), Flexbox (nav, tarjetas), breakpoint 768px
- **Iconos SVG inline**: 6 fragmentos, `aria-hidden="true"` (decorativos)
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

## 11. Datos de prueba

Comando `populate_news` crea:
- 3 categorías: Tecnología, Deportes, Cultura (con descripciones)
- 3 autores: Ana García, Carlos López, María Rodríguez
- 6 artículos (2 por categoría) con fechas escalonadas

## 12. Tests

```bash
# Verificación de configuración
python manage.py check

# Tests
python manage.py test

# Prueba escapado automático (manual)
# 1. Crear artículo con HTML: <script>alert("XSS")</script><b>negrita</b>
# 2. Ver en /articulo/<slug>/ → HTML mostrado como texto, no ejecutado
```

## 13. Observaciones

- El motor de plantillas cubre herencia (`extends`), fragmentos (`include`), variables, control (`for`, `empty`), filtros (`date`, `truncatewords`, `linebreaks`)
- El contenido gestionado desde el admin se ve en el portal sin tocar código
- La estructura de plantillas está ordenada y explicada en este README (sección 6)
- Las capturas del portal y admin deben tomarse manualmente para el entregable

---

**Autor**: [Nombre del alumno]
**Curso**: Desarrollo de Aplicaciones Empresariales, 4-C24-A
**Semana**: S06 - Motor de plantillas con Django