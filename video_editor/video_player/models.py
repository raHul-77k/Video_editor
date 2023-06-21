from django.db import models

class Effect(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    effect = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default='') # add default value here
    image_file = models.ImageField(upload_to='images', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails', null=True, blank=True)

    def __str__(self):
        return self.title
