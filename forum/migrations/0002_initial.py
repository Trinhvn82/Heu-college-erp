from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),  # Sửa lại số hiệu migration trước nếu khác
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='image',
            field=models.ImageField(upload_to='forum_images/', blank=True, null=True),
        ),
    ]