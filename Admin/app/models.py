from django.db import models
from django.contrib.auth.models import AbstractUser, User
import datetime
import os
import uuid

def filepath(instance, filename):
    # old_filename = filename
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    # timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    # filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)




class User(AbstractUser):
    file = models.FileField(upload_to=filepath, null=True,blank=True)


class Imageup(models.Model):
     filepath = models.ImageField(upload_to=filepath)
     filename = models.CharField(max_length=100)
     
class Category(models.Model):
    name = models.CharField( max_length =100,  null = True, blank=True)

class Product(models.Model):
    catid  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    imageid  = models.ForeignKey(Imageup, on_delete=models.CASCADE, related_name='product')

     

