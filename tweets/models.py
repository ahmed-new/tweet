from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class Post (models.Model):
    user= models.ForeignKey(User , on_delete=models.CASCADE , related_name='histweets')
    body= models.TextField(max_length=200)
    created= models.DateTimeField(auto_now= True)
    original_user=models.ForeignKey(User, on_delete=models.CASCADE , null=True ,blank=True)
    likes= models.ManyToManyField(User  , related_name='liked', blank=True )
   

    def __str__(self) :
        return self.user.username
    
    def likes_number(self):
        return self.likes.count()
    






class Profile(models.Model):
    user= models.OneToOneField(User , on_delete= models.CASCADE)
    follows= models.ManyToManyField('self' , related_name='followed_by' , symmetrical=False ,blank=True)
    updated= models.DateTimeField(auto_now_add=True)
    bio=models.TextField(max_length=200 , blank=True, null=True)
    image= models.ImageField(blank=True , null= True , upload_to='images/')

    def __str__(self):
        return self.user.username
    
    def following_count(self):
        return self.follows.count()
    
    def followers_count(self):
        return self.followed_by.count()



def create_profile(sender, instance, created , **kwargs):
    if created:
        user_profile= Profile(user= instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)      


class Comment (models.Model):
    post= models.ForeignKey(Post ,related_name='comments', on_delete= models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    body= models.TextField()
    date_added= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s - %s' % (self.post.user, self.name)


class Notification (models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    type= models.CharField(max_length=200)
    time= models.DateTimeField(auto_now_add=True)
    is_read= models.BooleanField(default=False)


    def __str__(self):
        return f'Notification for {self.user.username} : {self.type}'