# Generated by Django 4.2 on 2023-04-16 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_player', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
