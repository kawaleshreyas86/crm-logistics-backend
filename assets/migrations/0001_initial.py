from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A friendly name or label for the vehicle', max_length=255)),
                ('registration_number', models.CharField(max_length=50, unique=True)),
                ('vehicle_type', models.CharField(help_text='e.g. Truck, Van, Bike', max_length=100)),
                ('make', models.CharField(help_text='Brand/manufacturer e.g. Tata, Ashok Leyland', max_length=100)),
                ('model', models.CharField(help_text='Model name e.g. 407, Prima', max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('fuel_type', models.CharField(
                    choices=[('petrol', 'Petrol'), ('diesel', 'Diesel'), ('electric', 'Electric'),
                             ('cng', 'CNG'), ('hybrid', 'Hybrid')],
                    default='diesel', max_length=20)),
                ('capacity_kg', models.DecimalField(blank=True, decimal_places=2, help_text='Load capacity in kilograms',
                                                    max_digits=10, null=True)),
                ('status', models.CharField(
                    choices=[('active', 'Active'), ('inactive', 'Inactive'), ('maintenance', 'Under Maintenance')],
                    default='active', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='vehicles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
