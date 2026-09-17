from django.db import migrations


class Migration(migrations.Migration):
    """Transfiere el estado de negocio a sus aplicaciones de dominio.

    Las tablas mantienen sus nombres ``core_*`` para conservar datos y evitar
    operaciones DDL durante el despliegue.
    """

    dependencies = [
        ('core', '0001_initial'),
        ('productos', '0001_adopt_core_producto'),
        ('ventas', '0001_adopt_core_ventas'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name='DetallePedido'),
                migrations.DeleteModel(name='Pedido'),
                migrations.DeleteModel(name='Producto'),
            ],
        ),
    ]
