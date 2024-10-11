import os
import PIL
import PIL.Image
import PIL.ImageOps
from PIL import Image, ImageFilter
from django.shortcuts import redirect, render

from CIS4517CourseProject.settings import MEDIA_ROOT
from .forms import ImageUpload
from .models import ImageList

# Create your views here.
def index (request):
    if(request.method=="POST"):
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            process(image.id)
            return redirect("download", image_id=image.id)
        else:
            #change this to a redirect to some error page
            print("error")

    return render(request, 'app/index.html')

def process(id):
    image = ImageList.objects.get(id = id)
    img = Image.open(image.preprocessingFile.path)
    imgSplitPath = os.path.splitext(image.preprocessingFile.path)
    withinSplitFolder = os.path.split(imgSplitPath[0])[-1]
    modifiedImg = None

    if image.filterName == "Blur":
        if img.mode != "RGB":
            img = img.convert("RGB")
        modifiedImg = img.filter(ImageFilter.GaussianBlur)
    elif image.filterName == "Grayscale":
        modifiedImg = PIL.ImageOps.grayscale(img)
    elif image.filterName == "Poster":
        if img.mode != "RGB":
            img = img.convert("RGB")
        modifiedImg = PIL.ImageOps.posterize(img, 4)
    elif image.filterName == "Edge":
        if img.mode != "RGB":
            img = img.convert("RGB")
        modifiedImg = img.filter(filter=ImageFilter.FIND_EDGES)
    elif image.filterName == "Solar":
        if img.mode != "RGB":
            img = img.convert("RGB")
        modifiedImg = PIL.ImageOps.solarize(img, 64)
    img.close()

    saveFilePath = os.path.join(MEDIA_ROOT, 'filtered', withinSplitFolder + "_" + image.filterName + imgSplitPath[1])
    modifiedImg.save(saveFilePath)

    image.filteredFile = saveFilePath
    image.save()

    modifiedImg.close()
    

def download(request, image_id):
    image = ImageList.objects.get(id=image_id)
    return render(request, 'app/download.html', {'image' : image})

