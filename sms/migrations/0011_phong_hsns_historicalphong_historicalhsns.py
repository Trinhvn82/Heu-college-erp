# Generated by Django 4.2 on 2025-03-06 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sms', '0010_historicalhsgv_user_historicalhssv_user_hsgv_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hsns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ma', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('hoten', models.CharField(max_length=100)),
                ('diachi', models.CharField(blank=True, max_length=100)),
                ('quequan', models.CharField(blank=True, max_length=100)),
                ('sdt', models.CharField(blank=True, max_length=100)),
                ('gioitinh', models.CharField(blank=True, max_length=100)),
                ('cccd', models.CharField(blank=True, max_length=100)),
                ('ghichu', models.CharField(blank=True, max_length=500)),
                ('phong', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sms.phong')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPhong',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ten', models.CharField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical phong',
                'verbose_name_plural': 'historical phongs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalHsns',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ma', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('hoten', models.CharField(max_length=100)),
                ('diachi', models.CharField(blank=True, max_length=100)),
                ('quequan', models.CharField(blank=True, max_length=100)),
                ('sdt', models.CharField(blank=True, max_length=100)),
                ('gioitinh', models.CharField(blank=True, max_length=100)),
                ('cccd', models.CharField(blank=True, max_length=100)),
                ('ghichu', models.CharField(blank=True, max_length=500)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('phong', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sms.phong')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical hsns',
                'verbose_name_plural': 'historical hsnss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
