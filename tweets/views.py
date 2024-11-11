from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
from .models import Post , Profile , Comment , Notification
from django.contrib.auth . models import User
from .froms import Posrform , Commentform
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.views.generic import CreateView
from .froms import Signupform ,UserForm ,ProfileForm
from django.urls import reverse_lazy , reverse
import requests
from django.conf import settings
from django.core.signing import Signer , BadSignature
from django.core.mail import send_mail




def creat_post(request):
    if request.user.is_authenticated:
        generated_text = None
        

        url= "https://api.textsynth.com/v1/engines/mistral_7B/completions"
        headers = {"Authorization" : "Bearer b6605482a37831e2abf44ece13a49a5e"}
        
        if request.method=='POST' and 'prompt' in request.POST:
            
            prompt= request.POST.get('prompt' )
            data = {
                "prompt":f"type social tweet about {prompt}",
                "max_token":100
            }
            response= requests.post(url,headers=headers,json=data)
            if response.status_code == 200:
                generated_text= response.json().get('text', '')
                return render(request,'creat_post.html' ,{'generated_text' : generated_text})
        
    

        elif request.method == 'POST' and 'post_content' in request.POST:
            post_content = request.POST.get('post_content')
            tweet= Post.objects.create(user=request.user, body=post_content)
            tweet.save()
            return redirect('home')
        return render(request,'creat_post.html' ,{'generated_text' : generated_text})
    messages.error(request,'You Are not logged in')
    return redirect('home')     
            






   



def edit_post(request,pk):
    tweet= get_object_or_404(Post , id=pk)
    if request.user.is_authenticated:
        if request.user.username==tweet.user.username:
            form= Posrform(request.POST or None, instance=tweet)
            if request.method== 'POST':
                if form.is_valid():
                    tweet=form.save(commit=False)
                    tweet.user= request.user 
                    tweet.save()
                    messages.success(request,(' your tweet was Updated'))
                    return redirect('home')

            else:

                return render(request, 'edit_post.html', {'form':form })
            
        else:
            messages.error(request, "you are not authorized to take this action")
            return redirect('home')

    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login')



def delete_post(request,pk):
    tweet= get_object_or_404(Post , id=pk)
    if request.user.is_authenticated:
        if request.user.username==tweet.user.username:
            tweet.delete()
            messages.success(request ,'this tweet has been deleted')
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(request, "you are not authorized to take this action")
            return redirect('home')
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login')



def share_post(request,pk):
    tweet= get_object_or_404(Post , id=pk)
    new_post=Post.objects.create(user=request.user , body=tweet.body , original_user=tweet.user)
    new_post.save()
    message= f'{request.user} shared your tweet on his profile'
    Notification.objects.create(user=tweet.user , type=message )

    messages.success(request ,'This Tweet Was Shared  On Your Profile')
    return redirect(request.META.get("HTTP_REFERER"))


def post_like(request,pk):
    if request.user.is_authenticated:
        tweet= get_object_or_404(Post,id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
            message= f'{request.user} Liked your tweet 👍'
            Notification.objects.create(user=tweet.user , type=message)


        return redirect(request.META.get("HTTP_REFERER"))
    messages.error(request, "You must be logged in to view this page.")
    return redirect('login')
        




def update_profile(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(User, id=request.user.id)
        current_profile= Profile.objects.get(user__id= request.user.id)
        
        if request.method == 'POST':
            user_form = UserForm (request.POST or None,request.FILES or None, instance=current_user)
            profile_form= ProfileForm (request.POST or None,request.FILES or None, instance=current_profile)
            if  user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Your profile has been updated.")
                return redirect('home')
            else:
                messages.error(request, "There was an error updating your profile. Please try again.")
        else:
        
            user_form = UserForm(instance=current_user)
            profile_form = ProfileForm(instance=current_profile)
        
        return render(request, 'update_profile.html', {'user_form': user_form , 'profile_form':profile_form})
    
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login')
                




class Sign_up(CreateView):
    form_class= Signupform
    template_name = 'register.html'
    #success_url = reverse_lazy('login')
    def form_valid(self, form):
        user= form.save(commit=False)
        user.is_active= False
        user.save()
        signer= Signer()
        token= signer.sign(user.pk)
        activation_link= self.request.build_absolute_uri(
            reverse('activate',kwargs={'token':token})
        )
        subject = 'Activate your account in Tweet'
        email_content = f'''
    <html>
        <body>
            <h1>Hello {user.username},</h1>
            <p>Please click on the link below to activate your account 😊:</p>
            <p><a href="{activation_link}">Activate Account</a></p>
        </body>
    </html>
    '''
        #message = f'Hello {user.username} \n\n Please click on the link below to activate your account 😊 \n\n {activation_link}'
        message=''
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email] , html_message=email_content)
        messages.success(self.request,f'We Sent a confirmation link To {user.email} \n please check your inbox ')
        return redirect('register')

def confirm_email(request,token):
    signer=Signer()
    try:
        user_id = signer.unsign(token)
        user = User.objects.get(pk = user_id)
        user.is_active= True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request , user)
        messages.success (request, f'Thank you {user.username} for activating your account , Enjoy 😊 ')
        return redirect('home')
    except (BadSignature, User.DoesNotExist):
        messages.error (request, ' activation link not valid!')
        return redirect('register')







def login_user(request):
    
    if request.method== 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user= authenticate(request ,username=username ,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, (f'Welcome back {username}'))
            return redirect('home') 
        else:
            messages.success(request, ("There was an error logging in. Please Try Again..."))
            return redirect('login')

    else:
        return render(request, "login.html", {})





def logout_user(request):
    
    user_name= request.user.username

    logout(request)
    messages.success(request, (f"You Have Been Logged Out , goodby {user_name} ! "))
    return redirect('home')





def home(request):
    
    if request.user.is_authenticated:
        try:
            current_profile=Profile.objects.get(user__id=request.user.id)
            #tweets= Post.objects.all ().order_by('-created')
            tweets= Post.objects.filter(user__profile__in= current_profile.follows.all()).order_by('-created')
            
        except Profile.DoesNotExist:
        
            tweets=Post.objects.none()
        form= Posrform(request.POST, None)
        if request.method== 'POST':
            if form.is_valid():
                tweet=form.save(commit=False)
                tweet.user= request.user 
                tweet.save()
                followers= current_profile.followed_by.all()
                message= f'{request.user}  : Posted a tweet '
                for follower in followers:
                    Notification.objects.create(user=follower.user , type= message)


                messages.success(request,(' your tweet was shared to others'))
                return redirect ('home')

        else:

           return render(request, 'home.html', {'tweets':tweets, 'form':form})
    else:
        tweets = Post.objects.all().order_by('-created')
        return render(request, 'home.html', {'tweets':tweets})


def show_profile(request,pk):
    if request.user.is_authenticated:
        profile= Profile.objects.get(user_id=pk)
        tweets= Post.objects.filter (user_id=pk).order_by('-created')
        following_count= profile.following_count()
        followers_count= profile.followers_count()
        
        if request.method== 'POST':
            result= request.POST['follow']
            if result== 'unfollow':
                request.user.profile.follows.remove(profile)
            else :
                request.user.profile.follows.add(profile)



        return render(request,'profile.html',{'profile':profile ,'tweets':tweets ,'following_count':following_count ,'followers_count':followers_count})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')	
    


def profiles_list(request):
    profiles= Profile.objects.all()
    response = None
    if request.method== 'POST' and 'searched'in request.POST:
        query= request.POST['searched']
        profiles=Profile.objects.filter(user__username__startswith=query)
        if not profiles:
            response=f'({query})  not found , plz make sure of username'

    elif request.method== 'POST':
        pro_id= request.POST.get('profile_id')
        result= request.POST['follow']
        profile=get_object_or_404(Profile, id=pro_id)
        
        if result== 'unfollow':
            request.user.profile.follows.remove(profile)
        else :
            request.user.profile.follows.add(profile)
            message=f'{request.user.username} Followed You '
            Notification.objects.create(user=profile.user , type=message)


    return render( request,'profiles_list.html',{'profiles':profiles ,'response':response})




def add_comment(request,pk):
    tweet= get_object_or_404(Post,id=pk)
    current_pro= Profile.objects.get(user__id=request.user.id)
    if request.user.is_authenticated:
        form= Commentform(request.POST or None)
        if request.method== 'POST':
            if form.is_valid():
                
                com=form.save(commit=False)
                com.post = tweet
                com.name= request.user.username
                com.profile= current_pro
                com.save()
                message=f'{request.user.username} typed a comment on your tweet'
                Notification.objects.create(user=tweet.user , type=message)

                messages.success(request,('your comment has beed added'))
                return redirect ('home')

        else:

           return render(request, 'add_comment.html', {'form':form})


def notifications(request):
    notifications= Notification.objects.filter(user = request.user).order_by('-time')
    notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'notifications.html', {
        'notifications': notifications,
        'notifications_count': notifications_count,
    })

# views.py

def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')
