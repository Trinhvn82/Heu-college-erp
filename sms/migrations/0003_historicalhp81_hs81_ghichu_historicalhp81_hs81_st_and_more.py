# Generated by Django 4.2 on 2025-02-19 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_rename_ghichu1_historicalhp81_ghichu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalhp81',
            name='hs81_ghichu',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='historicalhp81',
            name='hs81_st',
            field=models.CharField(choices=[('Thiếu', 'Thiếu'), ('Đủ', 'Đủ')], default='Thiếu', max_length=20),
        ),
        migrations.AddField(
            model_name='hp81',
            name='hs81_ghichu',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='hp81',
            name='hs81_st',
            field=models.CharField(choices=[('Thiếu', 'Thiếu'), ('Đủ', 'Đủ')], default='Thiếu', max_length=20),
        ),
    ]
