# Generated by Django 5.1.2 on 2024-10-24 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0009_post_original_user_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tweets.profile'),
            preserve_default=False,
        ),
    ]
