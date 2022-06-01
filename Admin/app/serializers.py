from rest_framework import serializers
from app.models import User,Imageup, Category


class ImageSerializer(serializers.ModelSerializer):
    


    class Meta:
        model = Imageup
        fields = "__all__"
        
        
        



     


