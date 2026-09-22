from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_crm_groups(**kwargs):
    for name in ('admin', 'empleado'):
        Group.objects.get_or_create(name=name)
