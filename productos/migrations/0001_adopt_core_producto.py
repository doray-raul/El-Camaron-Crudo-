from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    """Adopta la tabla existente sin crearla ni copiar datos."""

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
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
                        'db_table': 'core_producto',
                        'ordering': ['nombre'],
                        'verbose_name': 'producto',
                        'verbose_name_plural': 'productos',
                    },
                ),
            ],
        ),
    ]
