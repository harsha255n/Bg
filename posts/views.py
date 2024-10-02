from django.shortcuts import render,redirect
from posts.forms import registerform,signform,Blogform,profileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from posts.models import Blog,profile
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound
from django.contrib import messages
from posts.forms import profileedit, passwordchange
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash



# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**store):
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            return fn(request,*args,**store)
    return wrapper

def mylogin(fn):
    def wrapper(request,*args,**store):
        id=store.get("pk")
        obj=Blog.objects.get(id=id)
        if obj.author !=request.user:
            return redirect("login")
        else:
            return fn(request,*args,**store)
    return wrapper 




class register_view(View):
    def get(self,request,*args,**store):
        data=registerform()
        return render(request,"registration.html",{"data":data})
    
    def post(self,request,*args,**store):
         data=registerform(request.POST)
         if data.is_valid():
             print(data.cleaned_data)
             User.objects.create_user(**data.cleaned_data) 
             return redirect("login")
         else: 
             print() 
         data=registerform()
         return render(request,"registration.html",{"reg":data})
      
class sign_view(View):
    def get(self,request,*args,**store):
     data=signform()
     return render(request,"sign.html",{"sign":data})
    
    def post(self,request,*args,**store):
        data=signform(request.POST)
        if data.is_valid():
            print(data.cleaned_data)
            u_name=data.cleaned_data.get("username")
            pasw=data.cleaned_data.get("password")

            user_obj=authenticate(request,username=u_name,password=pasw)
            if user_obj:
               login(request,user_obj)
              
               return redirect("blog_list")
               
            else:
                print("user id not valid")  
                messages.error(request, "User ID not valid") 
            return redirect("login")  
        

class sign_out(View):
    def get(self,request,*args,**store):
        logout(request)
        return redirect("login")
    


#profile


# @method_decorator(signin_required,name='dispatch')        
# class profileview(CreateView):
#     model = profile
#     form_class = profileForm
#     template_name = 'registration.html'  
#     success_url = reverse_lazy('profile_create')  

#     def form_valid(self, form):
#         form.instance.name = self.request.user  
#         return super().form_valid(form)  
#     def get_queryset(self):
        
#         return profile.objects.filter(user=self.request.user)
  
      
@method_decorator(signin_required,name='dispatch')           
class profile_Update(UpdateView):
    model = profile
    form_class = profileForm      
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile_view')
    def get_object(self, queryset=None):
        return profile.objects.get(user=self.request.user) 


class profile_view(View):
   
      def get(self,request,*args,**kwargs):
          qs=profile.objects.get(user=request.user)
          return render(request, "profile_view.html", {"profile": qs})
      
#user  edit

class User_edit_View(UpdateView):
    model = User
    form_class =  profileedit
    template_name = 'user_update.html'
    success_url = reverse_lazy('profile_view')  

    def get_object(self, queryset=None):
        return self.request.user

@login_required
def update_password(request):
    if request.method == 'POST':
        password_form =  passwordchange(request.POST)
        if password_form.is_valid():
            user = request.user
            if user.check_password(password_form.cleaned_data['old_password']):
                user.set_password(password_form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  
                messages.success(request, 'Your password has been updated successfully.')
                return redirect('login') 
            else:
                messages.error(request, 'Old password is incorrect.')
    else:
        password_form =  passwordchange()

    context = {
        'password_form': password_form,
    }
    return render(request, 'update_password.html', context)


    

#blog
      
@method_decorator(signin_required,name='dispatch')   
class blog_creation(View):
     def get(self,request,*args,**kwargs):
        data=Blogform()
        return render(request,"blog_creation.html",{"blog":data})
     

     def post(self,request,*args,**kwargs):
          data=Blogform(request.POST)
          if data.is_valid():
               print(data.cleaned_data)
               data = data.save(commit=False)
               data.author = request.user
               data.save()
               return redirect('blog_list')  
          return render(request, "blog_creation.html", {"blog": data})
     


      
@method_decorator(signin_required,name='dispatch')   
class blog_list(View):
   
      def get(self,request,*args,**kwargs):
          
          data=Blog.objects.filter(author=request.user)
          prod=profile.objects.get(user=request.user)
          return render(request, "home.html", {"blog_data": data,"profile": prod})



    
@method_decorator(mylogin,name='dispatch') 
class blog_single(View):
   
      def get(self,request,*args,**kwargs):
          id=kwargs.get("pk")
          data=Blog.objects.filter(id=id)
          return render(request, "blog_single.html", {"data": data,})    
      

@method_decorator(mylogin,name='dispatch') 
class blog_delete(View):
    def get(self,request,*args,**store):
        id=store.get("pk")
        Blog.objects.filter(id=id).delete()        
        return redirect("blog_list") 

@method_decorator(mylogin,name='dispatch') 
class blog_update(View):

    def get(self, request, *args, **store):
        id = store.get("pk")  
        blog = Blog.objects.filter(id=id).first()  
        
        if blog is None:
            return HttpResponseNotFound("Blog not found") 

        data = Blogform(instance=blog)  
        return render(request, "blog_update.html", {"data": data})

    def post(self, request, *args, **store):
        id = store.get("pk") 
        blog = Blog.objects.filter(id=id).first()  
        
        if blog is None:
            return HttpResponseNotFound("Blog not found")  

        data = Blogform(request.POST, instance=blog)  
        if data.is_valid():
            data.save()  
            return redirect('blog_list') 
        
        
        return render(request,"blog_update.html", {"data": data})
    

def search_blogs(request):
    query = request.GET.get('q')  
    results = []

    if query:
        if query.isdigit():
              results = Blog.objects.filter(id=query)
        else:          
            results = Blog.objects.filter(title__icontains=query)
        return render(request, 'blog_single.html', {'results': results, 'query': query})



