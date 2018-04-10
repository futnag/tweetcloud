from django.db import models
from datetime import datetime

class Cloud(models.Model):
    twitter_id = models.CharField(max_length=200, default='DEF_STRING')
    pic_name = models.CharField(max_length=200)
    # image = models.ImageField(upload_to="static/pictures/")
    created_at = models.DateTimeField(default=datetime.now, blank=True)
