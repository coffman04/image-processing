from django import forms 
from django.forms import FileField
from .models import ImageList

class ImageUpload(forms.ModelForm):
    class Meta:
        model = ImageList
        fields = ["preprocessingFile", "filterName"]

    
    
