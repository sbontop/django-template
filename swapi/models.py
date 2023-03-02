from django.db import models


# Create your models here.
class Person(models.Model):
    filename = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    # add any other relevant information here
