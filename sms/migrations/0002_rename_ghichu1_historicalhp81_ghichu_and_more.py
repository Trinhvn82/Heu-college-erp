# Generated by Django 4.2 on 2025-02-18 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalhp81',
            old_name='ghichu1',
            new_name='ghichu',
        ),
        migrations.RenameField(
            model_name='hp81',
            old_name='ghichu1',
            new_name='ghichu',
        ),
        migrations.RemoveField(
            model_name='historicalhp81',
            name='ghichu2',
        ),
        migrations.RemoveField(
            model_name='historicalhp81',
            name='status1',
        ),
        migrations.RemoveField(
            model_name='historicalhp81',
            name='status2',
        ),
        migrations.RemoveField(
            model_name='hp81',
            name='ghichu2',
        ),
        migrations.RemoveField(
            model_name='hp81',
            name='status1',
        ),
        migrations.RemoveField(
            model_name='hp81',
            name='status2',
        ),
        migrations.AddField(
            model_name='historicalhp81',
            name='status',
            field=models.ForeignKey(blank=True, db_constraint=False, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sms.hocphistatus'),
        ),
        migrations.AddField(
            model_name='hp81',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sms.hocphistatus'),
        ),
    ]
