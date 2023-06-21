# Generated by Django 4.2 on 2023-04-18 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_player', '0004_video_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('effect', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
