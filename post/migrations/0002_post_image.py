# Generated by Django 4.1 on 2022-08-19 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(default=None, upload_to="uploads/"),
            preserve_default=False,
        ),
    ]
