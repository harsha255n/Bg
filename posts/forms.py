from django import forms
from django.contrib.auth.models import User
from posts.models import profile
from posts.models import Blog
from django.contrib.auth.forms import UserChangeForm


class registerform(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password','email']


class signform(forms.Form):
   username=forms.CharField()
   password=forms.CharField()  

class profileForm(forms.ModelForm):
    class Meta:
        model=profile
        fields=['photo','user'] 
        widgets = {
            'photo': forms.FileInput(),  
        } 



class Blogform(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma separated tags'}),
        }    





class profileedit(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class passwordchange(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password')
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("The two password fields must match.")