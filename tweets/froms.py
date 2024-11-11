from django import forms
from .models import Post , Comment , Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(label="Profile Picture")
    bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))

    class Meta:
        model = Profile
        fields = ['image','bio'] 









class Signupform (UserCreationForm):
    email= forms.EmailField(required=True)
    first_name= forms.CharField(max_length=100)
    last_name= forms.CharField(max_length=100)
    class Meta:
        model= User
        fields=('username','email','first_name','last_name','password1','password2' )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please insert a new one.")
        return email    




class Posrform(forms.ModelForm):
    body=forms.CharField(required=True ,widget=forms.widgets.Textarea(attrs={
        'class':'form-control',
        'placeholder':'share your thoughts',

        

    }), label='')

    class Meta:
        model= Post
        exclude=('user','likes','original_user',)


class Commentform(forms.ModelForm):
    body=forms.CharField(required=True ,widget=forms.widgets.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Add you comment ',

        

    }), label='')

    class Meta:
        model= Comment
        exclude=('post','name','profile')

