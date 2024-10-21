from io import BytesIO
import os
import PIL
import PIL.Image
import PIL.ImageOps
import boto3
from PIL import Image, ImageFilter
from django.shortcuts import redirect, render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from CIS4517CourseProject import settings
from CIS4517CourseProject.settings import MEDIA_ROOT
from .forms import ImageUpload
from .models import ImageList
from decouple import config

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
    file_name = image.preprocessingFile.name  # Get the file name

    with default_storage.open(file_name, 'rb') as file:
        img = Image.open(file)
        img.load()
    
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

    image_io = BytesIO()

    original_format = img.format if img.format else 'JPEG'  

    modifiedImg.save(image_io, format=original_format)
    image_io.seek(0)  

    filtered_file_name = f'filtered/{image.id}_{image.filterName}{os.path.splitext(file_name)[1]}'

    default_storage.save(filtered_file_name, ContentFile(image_io.read()))

    image.filteredFile = filtered_file_name
    image.save()

    modifiedImg.close()
    

def download(request, image_id):
    image = ImageList.objects.get(id=image_id)
    s3 = boto3.client(
        's3',
        aws_access_key_id = config('AWS_ACCESS_KEY'),
        aws_secret_access_key = config('AWS_SECRET_KEY'),
        region_name = 'us-east-2'
    )
    presignedUrl = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': config('AWS_BUCKET_NAME'), 'Key': image.filteredFile.name},
        ExpiresIn=3600
    )

    presignedDownload = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': config('AWS_BUCKET_NAME'), 'Key': image.filteredFile.name, 'ResponseContentDisposition': 'attachment'},
        ExpiresIn=3600
    )

    return render(request, 'app/download.html', {'imageUrl' : presignedUrl, 'imageDownload':presignedDownload})

