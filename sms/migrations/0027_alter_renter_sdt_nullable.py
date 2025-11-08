from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0026_historicalhoadon_qr_code_image_hoadon_qr_code_image'),
    ]

    operations = [
        # Safety: explicitly alter the column to drop NOT NULL if it exists
        migrations.RunSQL(
            sql="ALTER TABLE sms_renter ALTER COLUMN sdt DROP NOT NULL;",
            reverse_sql="ALTER TABLE sms_renter ALTER COLUMN sdt SET NOT NULL;"
        ),
        migrations.AlterField(
            model_name='renter',
            name='sdt',
            field=models.CharField(max_length=100, blank=True, null=True, verbose_name='Số điện thoại'),
        ),
    ]
