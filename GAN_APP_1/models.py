from django.db import models

# Create your models here.
class Collection(models.Model):
    image_id = models.AutoField(primary_key = True)
    image_bytes = models.TextField(max_length = None)