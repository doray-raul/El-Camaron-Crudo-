from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


def cargar_productos_iniciales(apps, schema_editor):
    Producto = apps.get_model('core', 'Producto')
    Producto.objects.bulk_create([
        Producto(
            nombre='Ceviche de Camarón',
            descripcion='Fresco y picante, con nuestro toque especial.',
            precio='120.00',
            imagen='img/Logo.jpeg',
        ),
        Producto(
            nombre='Camarones al Ajillo',
            descripcion='Salteados con ajo y mantequilla, una delicia.',
            precio='150.00',
            imagen='img/Producto1.jpeg',
        ),
        Producto(
            nombre='Producto Fresco',
            descripcion='Selección de mariscos frescos del día.',
            precio='180.00',
            imagen='img/Producto2.jpeg',
        ),
    ])


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])),
                ('imagen', models.CharField(help_text='Ruta dentro de core/static, por ejemplo img/Producto1.jpeg', max_length=255)),
                ('disponible', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'productos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cliente', models.CharField(max_length=150)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(blank=True, max_length=25)),
                ('direccion', models.TextField(blank=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])),
                ('costo_envio', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[MinValueValidator(0)])),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('PAGADO', 'Pagado'), ('EN_PREPARACION', 'En preparación'), ('ENTREGADO', 'Entregado'), ('CANCELADO', 'Cancelado')], default='PENDIENTE', max_length=20)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-creado_en']},
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=120)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])),
                ('cantidad', models.PositiveIntegerField(validators=[MinValueValidator(1)])),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='core.pedido')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detalles_pedido', to='core.producto')),
            ],
            options={
                'verbose_name': 'detalle de pedido',
                'verbose_name_plural': 'detalles de pedido',
            },
        ),
        migrations.RunPython(cargar_productos_iniciales, migrations.RunPython.noop),
    ]
