from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def vincular_clientes_con_usuarios(apps, schema_editor):
    Cliente = apps.get_model('crm', 'Cliente')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    for cliente in Cliente.objects.filter(usuario__isnull=True).exclude(correo=''):
        usuario = User.objects.filter(email__iexact=cliente.correo).first()
        if usuario and not Cliente.objects.filter(usuario=usuario).exists():
            cliente.usuario = usuario
            cliente.save(update_fields=['usuario'])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0003_rename_etapa_cliente_etapa_crm'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='perfil_cliente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(vincular_clientes_con_usuarios, migrations.RunPython.noop),
    ]
