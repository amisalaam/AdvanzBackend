# Generated by Django 4.2.2 on 2023-07-11 04:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctor', '0004_alter_slots_is_booked_appiontment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('completed', 'Completed')], default='Pending', max_length=10)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.slots')),
            ],
        ),
        migrations.DeleteModel(
            name='Appiontment',
        ),
    ]
