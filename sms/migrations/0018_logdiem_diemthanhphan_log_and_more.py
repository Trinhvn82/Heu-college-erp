# Generated by Django 4.2 on 2025-03-10 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0017_historicalhs81_gks_hs81_gks'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogDiem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='diemthanhphan',
            name='log',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sms.logdiem'),
        ),
        migrations.AddField(
            model_name='historicaldiemthanhphan',
            name='log',
            field=models.ForeignKey(blank=True, db_constraint=False, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sms.logdiem'),
        ),
    ]
