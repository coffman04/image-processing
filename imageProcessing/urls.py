from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("uploadFile", views.index, name='index'),
    path("download", views.download, name='download')
]