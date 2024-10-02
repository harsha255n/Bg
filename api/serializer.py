from django.contrib.auth.models import User
from rest_framework import serializers
from posts.models import Blog,profile

class userserializer(serializers.ModelSerializer):
    class Meta:
        model=User 
        fields=["id","username","email","password"]
        read_only_fields=["id"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    

class Blogserial(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields = ['id','title','content','created_at']


class profileserial(serializers.ModelSerializer):
    class Meta:
        model=profile
        fields=['id','photo']  \
        








class Userserial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)  
        
        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        instance.save()
        return instance