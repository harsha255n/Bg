from django.contrib import admin
from posts import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from posts.views import profile_Update,User_edit_View,update_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",views.register_view.as_view(),name="register"),
    path("login/",views.sign_view.as_view(),name="login"),
    path('logout/',views.sign_out.as_view(),name="logout"),
    path("blog/",views.blog_creation.as_view(),name="blog_create"),
    path("home/",views.blog_list.as_view(),name="blog_list"),
    path('profileupdate/', profile_Update.as_view(), name='profile_update'),
    path('yourprofilr/', views.profile_view.as_view(), name='profile_view'),
    path('blogdetail/<int:pk>', views.blog_single.as_view(), name='blog_view'),
    path('blogdelete/<int:pk>',views.blog_delete.as_view(), name='blog_delete'),
    path('blogupdate/<int:pk>',views.blog_update.as_view(), name='blog_update'),
    path('updateprofile/', User_edit_View.as_view(), name='profilechange'),
    path('updateps/', update_password, name='update_password'),
    path('search/', views.search_blogs, name='search_blogs'),
    # path('profileview/',profileview.as_view(), name='profile_create')
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)