# Generated by Django 4.1.4 on 2022-12-21 14:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_channel_options_channel_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='channel_image',
            field=models.ImageField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])]),
        ),
        migrations.AddField(
            model_name='content',
            name='content_file',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['mp4', 'mov', 'avi', 'pdf', 'txt'])]),
        ),
        migrations.AddField(
            model_name='content',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=1.1, max_digits=3),
            preserve_default=False,
        ),
    ]
