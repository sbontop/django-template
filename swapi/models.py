from django.db import models


class Dataset(models.Model):
    file_name = models.CharField(max_length=255)
    download_date = models.DateTimeField(auto_now_add=True)
    num_characters = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
