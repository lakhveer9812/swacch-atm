from app import views
from django.urls import path

urlpatterns =[
    path("", views.Login, name="login"),
    path("list", views.imgList, name="list"),
    path("assign-category", views.assignCategory, name="assign-category"),
    path("imageupload", views.ImageUpload.as_view(), name="imageupload"),
    path('login', views.LoginAPI.as_view()),
    # path("list", views.List, name="list"),

]