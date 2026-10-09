# Agentes del Laboratorio

## Orquestador
Dirige el flujo de trabajo, valida hallazgos y decide próximos pasos.
- Revisa los informes de los subagentes
- Presenta diagnósticos al usuario
- Aprueba o ajusta planes antes de programación

## Programmer
Implementa el código Python/Django según lo definido.
- Crea la app `movies`: modelos, migraciones y vistas
- Configura el administrador con `ModelAdmin`, `RatingInline` y `readonly_fields`
- Crea el grupo `editores` con una migración de datos
- Ejecuta migraciones y tests, y aplica PEP 8

## Documentor
Audita requisitos, rúbrica y evidencia del laboratorio.
- Verifica que cada paso de la guía esté cubierto
- Carga los datos de prueba desde el panel y toma las capturas antes/después y superusuario vs editor
- NO modifica código

## Frontend
Configura plantillas y estructura visual.
- Catálogo con portadas y vista de recomendaciones
- Tailwind CSS para estilos responsivos

## Git-Github
Maneja el repositorio y los commits.
- Un commit por bloque de cambio, con mensaje en español que describe qué se modificó
- No sube `.env`, la base de datos, `media/` ni carpetas de herramientas locales
