from django.contrib import admin
from .models import Post ,Profile , Comment, Notification
from django.contrib.auth.models import User , Group 


admin.site.unregister(Group)
admin.site.register(Notification)


#admin.site.register(Profile)

class Profileinline(admin.StackedInline):

    model= Profile

class Useradmin(admin.ModelAdmin):
    model = User
    inlines = [Profileinline]
    fields=['username','email','first_name','last_name']

admin.site.unregister(User)
admin.site.register(User,Useradmin)
admin.site.register(Post)
admin.site.register(Comment)




