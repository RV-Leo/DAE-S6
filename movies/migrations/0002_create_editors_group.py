from django.contrib.auth.management import create_permissions
from django.db import migrations

GROUP_NAME = 'editores'

# Editors keep the catalog up to date but cannot delete anything:
# they add/change movies and their ratings, and only view genres and people.
EDITOR_PERMISSIONS = [
    'add_movie', 'change_movie', 'view_movie',
    'add_rating', 'change_rating', 'view_rating',
    'view_genre',
    'view_person',
]


def create_editors_group(apps, schema_editor):
    # Permissions are normally created after migrate; make sure they exist now.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    group, _ = Group.objects.get_or_create(name=GROUP_NAME)
    group.permissions.set(
        Permission.objects.filter(content_type__app_label='movies', codename__in=EDITOR_PERMISSIONS)
    )


def delete_editors_group(apps, schema_editor):
    apps.get_model('auth', 'Group').objects.filter(name=GROUP_NAME).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_editors_group, delete_editors_group),
    ]
