from rest_framework.routers import DefaultRouter
from api.views import SignUpView
from django.urls import path
from api.views import blogview,profileview,Userprofile
from rest_framework.authtoken.views import ObtainAuthToken


router=DefaultRouter()
router.register("v2/blog",blogview,basename="task")
router.register("v2/profile",profileview,basename="profile")
router.register("v2/user",Userprofile,basename="user")




urlpatterns=[
    path("token/",ObtainAuthToken.as_view()),
    path("register/",SignUpView.as_view())
]+router.urls