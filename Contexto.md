# Contexto del Proyecto — Semana 5: "Administrador con Django"

## Objetivo

Gestionar un catálogo de películas desde el administrador de Django: modelos relacionados,
personalización con `ModelAdmin` y control de acceso con usuarios, grupos y permisos.

## Contexto del laboratorio

El proyecto es **acumulativo**: parte del resultado de la semana 4 (app `library`) y añade la app `movies`.

## Criterios de evaluación (20 puntos)

| # | Criterio | Puntos |
|---|----------|--------|
| 1 | Configura el administrador para gestionar los modelos relacionados | 5 |
| 2 | Personaliza listado, filtros y búsqueda con ModelAdmin | 5 |
| 3 | Administra el acceso con usuarios, grupos y permisos | 5 |
| 4 | Entrega el repositorio con la configuración del panel y sus observaciones | 5 |

## Requerimientos específicos

1. Declarar la app `movies` en `INSTALLED_APPS` e instalar Pillow.
2. Modelos `Movie`, `Genre`, `Person` y `Rating` con campos, `Meta` y `__str__` (Movie↔Genre N:M, Rating→Movie FK).
3. Migraciones y superusuario.
4. Registro simple en `admin.py` y comprobar el CRUD sin vistas.
5. `ModelAdmin` con `list_display`, `list_filter` (género, año) y `search_fields` (título, nombre).
6. Valoraciones como inline dentro de la película.
7. Campos de auditoría de solo lectura.
8. Datos de prueba: 10 películas, 4 géneros y valoraciones en al menos 5.
9. Grupo «editores» (añadir y cambiar películas, sin eliminar) y usuario de prueba.
10. Vista pública de recomendación: películas del mismo género mejor valoradas.
11. Capturas antes/después y superusuario vs editor.
12. Subir el proyecto al repositorio y el entregable al campus.

## Normas

- Código Python según PEP 8
- Estructura Django: una aplicación por responsabilidad
- Modelos en singular, migraciones versionadas
- settings.py sin credenciales escritas a mano
- Código, nombres de variables y comentarios en **inglés**
- Entregables y explicaciones en **español**
