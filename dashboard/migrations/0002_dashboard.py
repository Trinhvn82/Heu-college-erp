# Generated by Django 4.2 on 2025-03-21 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ma', models.CharField(blank=True, default='', max_length=300)),
            ],
        ),
    ]
