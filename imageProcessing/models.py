from django.db import models

# Create your models here.

class ImageList(models.Model):
    preprocessingFile = models.ImageField(
        upload_to="images/"
    )
    filterName = models.TextField()
    filteredFile = models.ImageField(
        upload_to="filtered/"
    )

