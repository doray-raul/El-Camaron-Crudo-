from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crea o actualiza el administrador local admin.'

    def handle(self, *args, **options):
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@elcamaroncrudo.local',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        user.email = 'admin@elcamaroncrudo.local'
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password('admin123')
        user.save()
        action = 'creado' if created else 'actualizado'
        self.stdout.write(self.style.SUCCESS(f'Administrador {action}: admin'))
