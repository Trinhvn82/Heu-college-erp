# Generated by Django 4.2 on 2025-05-22 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0006_alter_diemthanhphan_diem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallopmonhoc',
            name='mhdk',
            field=models.BooleanField(default=False, verbose_name='Môn học điều kiện'),
        ),
        migrations.AddField(
            model_name='lopmonhoc',
            name='mhdk',
            field=models.BooleanField(default=False, verbose_name='Môn học điều kiện'),
        ),
    ]
