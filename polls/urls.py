from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path('imgurl/', views.imgurl, name='imgurl'),
]
