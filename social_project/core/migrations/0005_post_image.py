# Generated by Django 5.1.4 on 2025-01-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_profile_profile_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="post_images/"),
        ),
    ]
