# Generated by Django 5.1 on 2024-10-19 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CafeBooking', '0002_alter_office_address_alter_place_office_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время лога')),
                ('action', models.CharField(max_length=255, verbose_name='Действие')),
            ],
        ),
    ]
