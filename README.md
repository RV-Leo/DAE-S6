# Laboratorio 5 — Administrador con Django

Proyecto Django del Laboratorio 5 (Semana 5) que gestiona un catálogo de películas desde el administrador de Django. Continúa el proyecto de la semana 4 (app `library`) y añade la app `movies`.
## 1. Descripción

- Modelos relacionados `Movie`, `Genre`, `Person` y `Rating`, gestionados desde el panel sin escribir vistas.
- Personalización con `ModelAdmin`: listado, filtros, búsqueda, valoraciones en línea y campos de solo lectura.
- Control de acceso con el grupo `editores`.
- Catálogo público con portadas y vista de recomendación por género.

## 2. Tecnologías

- Python 3.12
- Django 6.1.1
- Pillow 12.3.0
- SQLite
- Tailwind CSS

## 3. Modelos y relaciones

- **Movie** — `title`, `year`, `synopsis`, `poster`, `created_at`, `updated_at`.
- **Genre** — `Movie.genres` (N:M): una película tiene varios géneros.
- **Person** — `Movie.director` (FK, `SET_NULL`): si se borra el director, la película se conserva.
- **Rating** — `Rating.movie` (FK, `CASCADE`): puntaje de 1 a 5.

## 4. Administrador

- `list_display` con año, director, géneros, promedio y número de valoraciones.
- `list_filter` por género y año; `search_fields` por título y director.
- `RatingInline` para registrar valoraciones desde el formulario de la película.
- `readonly_fields` en `created_at` y `updated_at`.

## 5. Roles y permisos

- **Superusuario**: acceso total.
- **editores**: añaden y modifican películas y valoraciones, pero no pueden eliminar ni gestionar usuarios. Eliminar es irreversible, por eso queda reservado al administrador.

El grupo se crea con la migración de datos `0002_create_editors_group`, así que existe al ejecutar `migrate`.

Comprobado con el usuario de prueba `editor1`: solo ve la sección Movies, no aparecen el botón Delete ni las casillas para borrar valoraciones, y la URL de borrado responde 403 (capturas 12 a 15).

## 6. Instalación y ejecución

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

En `.env` se define `DJANGO_SECRET_KEY`; `settings.py` no guarda credenciales.

- Administrador: `http://127.0.0.1:8000/admin/`
- Catálogo: `http://127.0.0.1:8000/movies/`
- Recomendaciones: `http://127.0.0.1:8000/movies/<id>/recommendations/`

## 7. Datos de prueba

Se cargaron desde el panel: 10 películas, 4 géneros (Acción, Ciencia ficción, Terror y Aventura) y valoraciones en 8 películas. Las portadas usadas están en `docs/portadas/`.

## 8. Tests

```bash
python manage.py test
```

## 9. Observaciones

- El administrador cubre el CRUD de todos los modelos sin escribir vistas; la recomendación por género se implementó como vista propia porque calcula promedios y es pública.
- Las capturas del panel (antes/después y superusuario vs editor) están en `docs/evidencias/`.
