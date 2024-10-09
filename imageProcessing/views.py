import os
import PIL
import PIL.Image
import PIL.ImageOps
from PIL import Image, ImageFilter
from django.shortcuts import redirect, render
from .forms import ImageUpload, FilterUpload
from .models import ImageList

# Create your views here.
def index (request):
    if(request.method=="POST"):
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            #image = form.save()
            #process(image.id)
            return redirect("download")
            # return redirect("download", image.id)
        else:
            #change this to a redirect to some error page
            print("error")

    return render(request, 'app/index.html')

def process(id):
    image = ImageList.get(id = id)
    img = Image.open(image.preprocessingFile.path)
    imgSplitPath = os.path.splitext(image.preprocesssingFile.path)
    withinSplitFolder = imgSplitPath[0].split('/')[-1]
    filteredLoc = os.path.join(withinSplitFolder + "_" + image.filterName + imgSplitPath[1])

    if image.filterName == "Blur":
        img = img.filter(filter=ImageFilter.BLUR)
    if image.filterName == "Grayscale":
        img = PIL.ImageOps.grayscale(img)
    if image.filterName == "Poster":
        img = PIL.ImageOps.posterize(img, 4)

    form = FilterUpload(img, instance=image)
    print("end of process")
    #if form.is_valid():
    #    form.save()

def download(request):
    return render(request, 'app/download.html')

