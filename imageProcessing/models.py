from django.db import models

# Create your models here.

class ImageList(models.Model):
    preprocessingFile = models.ImageField(
        upload_to="images/"
    )
    filterName = models.TextField()
    filteredFile = models.ImageField(
        upload_to="filtered/",
        blank=True,
        null=True
    )
    
    def __str__(self):
        if self.filteredFile != None:
            return f"{self.preprocessingFile.path}, {self.filterName}, {self.filteredFile.path}"
        else:
            return f"{self.preprocessingFile.path}, {self.filterName}"

