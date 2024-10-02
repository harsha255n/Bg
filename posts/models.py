from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

# Create your models here.


class profile(models.Model)  :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_pics', null=True,blank=True, default='profile_pics/r.jpeg')

    def __str__(self):
        return self.user.username 


class Blog(models.Model):   
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()  
    tags = TaggableManager(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title