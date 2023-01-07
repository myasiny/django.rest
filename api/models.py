from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import CASCADE


class Channel(models.Model):
    LOCALE = (
        ('en_EN', 'English'),
        ('sp_SP', 'Spanish'),
        ('tr_TR', 'Turkish'),
        ('ch_CH', 'Chinese'),
        ('ar_AR', 'Arabic'),
        ('fr_FR', 'French'),
    )

    title = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=5, choices=LOCALE, default=LOCALE[0][0])
    channel_image = models.ImageField(validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])])
    parent_channel = models.ForeignKey('self', related_name='child_channels', on_delete=CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at', 'created_at']


class Content(models.Model):
    TYPE = (
        ('history', 'History'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('fiction', 'Fiction'),
        ('action', 'Action'),
        ('horror', 'Horror'),
        ('drama', 'Drama'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(default='', blank=True, null=True)
    genre = models.CharField(max_length=7, choices=TYPE, default=TYPE[0][0])
    content_file = models.FileField(validators=[FileExtensionValidator(['mp4', 'mov', 'avi', 'pdf', 'txt'])])
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    channel = models.ForeignKey(Channel, related_name='contents', on_delete=CASCADE, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at', 'created_at']
