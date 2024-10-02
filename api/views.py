from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializer import userserializer
from rest_framework import permissions,authentication,status
from rest_framework.viewsets import ViewSet
from posts.models import Blog,profile
from api.serializer import Blogserial,profileserial,Userserial
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets

# Create your views here.

#registration

class SignUpView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

#Blog


class blogview(ViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Blog.objects.filter(author=request.user)
        serializer=Blogserial(qs,many=True)
        return Response(data=serializer.data)
    
    def create(self,request,*args,**kwargs):
        serializer=Blogserial(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
        return Response(data=serializer.data)  
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Blog.objects.get(id=id)
        serializer=Blogserial(data=request.data,instance=qs)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)   
        return Response(serializer.errors)
    
    def retrieve(self,request,*args,**kwargs):
         id=kwargs.get("pk")
         qs=Blog.objects.filter(id=id,author=request.user)
         serializer=Blogserial(qs,many=True)
         return Response(data=serializer.data)
    
   
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        qs = get_object_or_404(Blog, id=id, author=request.user)
        qs.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    #profile picture 
    #need subscribtions
    

class profileview(ViewSet):
     authentication_classes=[authentication.BasicAuthentication]
     permission_classes=[permissions.IsAuthenticated]

     def list(self,request,*args,**kwargs):
        qs=profile.objects.filter(user=request.user)
        serializer=profileserial(qs,many=True)
        return Response(data=serializer.data)

     def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=profile.objects.get(id=id)
        serializer=profileserial(data=request.data,instance=qs)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)   
        return Response(serializer.errors)
     

#user

class Userprofile(viewsets.ViewSet):
    authentication_classes = [authentication.BasicAuthentication]  
    permission_classes = [permissions.IsAuthenticated]

    
    def list(self, request):
        serializer = Userserial(request.user)
        return Response(serializer.data)

   
    def partial_update(self, request, pk=None):
        user = request.user
        serializer = Userserial(user, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
