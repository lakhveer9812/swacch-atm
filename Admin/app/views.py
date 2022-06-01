from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import ImageSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Imageup, User,Product,Category, filepath
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
import os, uuid
import shutil






# Create your views here.
def Login(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        superusers = User.objects.filter(is_superuser=True)
        if user  in superusers:
            login(request, user)
            return redirect('list')
        else:         
            messages.success(request, 'Incorrect Email or Password! Please Try Again.')
            return redirect('login')
    else:        
        return render(request, 'list.html')  

class LoginAPI(APIView):
    """
    Login Api view
"""


    def post(self, request, *args, **kwargs):

        context = dict()
        email = request.data.get('email')
        password = request.data.get('password')
        superusers = User.objects.filter(is_superuser=True)

        

        if email is None:
            status_code = status.HTTP_200_OK
            context['data'] = ""
            context['message'] = ""
            context['status'] = 401
            context['error'] = "Email is required"
        elif password is None:
            status_code = status.HTTP_200_OK
            context['data'] = ""
            context['message'] = ""
            context['status'] = 401
            context['error'] = "Password is required"
        else:
            try:
                user = User.objects.get(email=email)
                print(user)
            except Exception as e:
                status_code = status.HTTP_200_OK
                context['data'] = ""
                context['message'] = ""
                context['status'] = 402
                context['error'] = "User with this email does not Exist"
            else:
                if user.check_password(password) is False:
                    status_code = status.HTTP_200_OK
                    context['data'] = ""
                    context['message'] = ""
                    context['status'] = 401
                    context['error'] = "Incorrect Password"
                    # context['success'] = False

                elif user in superusers:
                    status_code = status.HTTP_200_OK
                    context['data'] = ""
                    context['message'] = ""
                    context['status'] = 401
                    context['error'] = "Incorrect Email or Password"
                else:

                    status_code = status.HTTP_200_OK
                    user = User.objects.get(email=email)
                    token, created = Token.objects.update_or_create(
                        user=user
                    )

                    context['status'] = status_code
                    context['Success'] = "true"
                    context['message'] = "User Login Successfully"
                    context['data'] = {"token": token.key, "name": user.username,
                                       "first_name": user.first_name, "last_name": user.last_name}

        return Response(context, status=status_code)



# def upload(request):
#     if request.method == 'POST':
#         files = request.FILES['file']
#         Imageup.objects.create(filename=files, filepath=files) 
#         return render(request, 'list.html')       

class ImageUpload(APIView):

    def post(self, request):
        context = {}
        try:
            # ext = filename.split('.')[-1]
            # filename = "%s.%s" % (uuid.uuid4(), ext)
            
            request.data['filename'] = str(request.data['filepath'])
            # print(request.data['filename'])
            ext = request.data['filename'].split('.')[-1]
            
            filename = "%s.%s" % (uuid.uuid4(), ext)
            print(filename,'abcaaaaaaaaadddddddddddddddddddddddffffffffff')
            request.data['filename']=filename
            serializer = ImageSerializer(data = request.data)
            if filepath is None:
                status_code = status.HTTP_200_OK
                context['data'] = ""
                context['message'] = ""
                context['status'] = 401
                context['error'] = "attachment is required"

            elif serializer.is_valid() is False:
                status_code = status.HTTP_400_BAD_REQUEST
                context['message'] = ""
                context['status'] = status_code
                context['error'] = serializer.errors
                context['data'] = ""
            else:
                status_code = status.HTTP_200_OK
                serializer.save()
                context['data'] = serializer.data
                context['status'] = status_code
                context['message'] = "uploaded"
        except Exception as e:
            status_code = status.HTTP_200_OK
            context['message'] = ""
            context['data'] = ""
            context['error'] = str(e)
            context['status'] = status_code

        return Response(context, status=status_code)


def imgList(request):
    list = Imageup.objects.all()
    print('aa gya me')
    print(list[0].product.first().catid.name)
    return render(request, "list.html", {'list': list})


def assignCategory(request):
    list = Imageup.objects.all()
    category = Category.objects.all()
    # print('aa gya me');
    # print(list[0].product.first().catid)


    if request.method == 'GET':
        return render(request, "assign-category.html", {'list': list, 'category': category})

    if request.method == 'POST':    
        imageids = request.POST.getlist('imageid[]')
        catid = request.POST['catid']
       

        for imageid in imageids:
            imgObj = Imageup.objects.get(id=imageid)
            catObj = Category.objects.get(id=catid)
            Product.objects.create(catid=catObj, imageid=imgObj)
          


            mediaPath = settings.MEDIA_ROOT
            catMediaPath = mediaPath + '/' + catObj.name
            if not os.path.exists(catMediaPath):
                os.mkdir(catMediaPath)

            filePath = str(imgObj.filepath)
            fileMediaPath = mediaPath + '/' + filePath
            if os.path.exists(fileMediaPath):
                newFileMediaPath = catMediaPath + '/' + imgObj.filename
                shutil.move(fileMediaPath, newFileMediaPath)
                imgObj.filepath = catObj.name + '/' + imgObj.filename
                imgObj.save() 
        
        return render(request, "assign-category.html",  {'list': list, 'category': category})          



  



# def Move(request):
#     if request.method == 'GET':
#         list = Imageup.objects.all()
#         print(list)
#         category = Category.objects.all()
#         return render(request, "list.html", {'list': list, 'category': category})
#     if request.method == 'POST':    
#                 imageids = request.POST.getlist('imageid[]')
#                 catid = request.POST['catid']
#                 for imageid in imageids:
#                     Product.objects.create(catid=catid, imageid=imageid)
#                     imgObj = Imageup.objects.get(id=imageid)
#                     catObj = Category.objects.get(id=catid)
                    
#                     mediaPath = settings.MEDIA_ROOT
#                     catMediaPath = mediaPath + '/' + catObj.name
#                     if not os.path.exists(catMediaPath):
#                         os.mkdir(catMediaPath)
                        
#                     filePath = str(imgObj.filepath)
#                     fileMediaPath = mediaPath + '/' + filePath
#                     if os.path.exists(fileMediaPath):
#                         newFileMediaPath = catMediaPath + '/' + imgObj.filename
#                         shutil.move(fileMediaPath, newFileMediaPath)
#                         imgObj.filepath = catObj.name + '/' + imgObj.filename
#                         imgObj.save()   
#                 return render(request, "assign-category.html")    

                        



# @api_view(['GET','POST'])
# def List(request):
#      if request.method == 'GET':
#           img = Imageup.objects.all()
#           serializer = ListSerializer(img, many = True)
#           return Response(serializer.data)

#      elif request.method == 'POST':
#          imageids = request.data.getlist('imageid[]')
#          catid = request.data.get('catid')
#          for imageid in imageids:
#               Product.objects.create(catid=catid, imageid=imageid)
#               imgObj = Imageup.objects.get(id=imageid)
#               catObj = Category.objects.get(id=catid)
#               mediaPath = settings.MEDIA_ROOT
#               catMediaPath = mediaPath + '/' + catObj.name
#      return Response(serializer.data, status=status.HTTP_201_CREATED)
        #  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








    #  def get(self, request):
    #     context = {}
    #     try:
    #         status_code = status.HTTP_200_OK
    #         img = Imageup.objects.all()
    #         serializer = ListSerializer(img, many = True)
    #         context['data'] = serializer.data
    #         context['status'] = status_code
    #         context['message'] = "View List"
       
    #     except Exception as e:   
    #         status_code = status.HTTP_404_NOT_FOUND
    #         context['data'] = ""
    #         context['message'] = ""
    #         context['status'] = status_code
    #         context['error'] = str(e)
    #     return Response(context, status=status_code)


       

		 

          
        #     status_code = status.HTTP_200_OK
		# 	user = Imageup.objects.all()
		# 	serializer = ListSerializer(user, many=True)
        #     context['data'] = serializer.data
		# 	context['status'] = status_code
		# 	context['message'] = "View list"
		# except Exception as e:
		# 	status_code = status.HTTP_404_NOT_FOUND
		# 	context['data'] = ""
		# 	context['message'] = ""
		# 	context['status'] = status_code
		# 	context['error'] = str(e)

		# return Response(context, status=status_code)
            # list = Imageup.objects.all()
            # category = Category.objects.all()
            # # print(category)
            # return Response(request,
            # # return render(request, "list.html", {'list': list,'category': category})
            # if request.method == "POST":
            #     imageids = request.POST.getlist('imageid[]')
            #     catid = request.POST['catid']
            #     for imageid in imageids:
            #         Product.objects.create(catid=catid, imageid=imageid)
            #         imgObj = Imageup.objects.get(id=imageid)
            #         catObj = Category.objects.get(id=catid)
                    
            #         mediaPath = settings.MEDIA_ROOT
            #         catMediaPath = mediaPath + '/' + catObj.name
            #         if not os.path.exists(catMediaPath):
            #             os.mkdir(catMediaPath)
                        
            #         filePath = str(imgObj.filepath)
            #         fileMediaPath = mediaPath + '/' + filePath
            #         if os.path.exists(fileMediaPath):
            #             newFileMediaPath = catMediaPath + '/' + imgObj.filename
            #             shutil.move(fileMediaPath, newFileMediaPath)
            #             imgObj.filepath = catObj.name + '/' + imgObj.filename
            #             imgObj.save()        
                
