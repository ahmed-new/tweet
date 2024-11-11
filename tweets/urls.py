
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:pk>', views.show_profile, name= 'profile'),
    path('profiles',views.profiles_list, name='profiles_list'),
    path('register',views.Sign_up.as_view(), name='register'),
    path('login',views.login_user, name='login'),
    path('logout',views.logout_user, name='logout'),
    path('update_profile',views.update_profile, name='update_profile'),
    path('like/<int:pk>', views.post_like, name= 'post_like'),
    path('share/<int:pk>', views.share_post, name= 'share'),
    path('delete/<int:pk>', views.delete_post, name= 'delete'),
    path('edit/<int:pk>', views.edit_post, name= 'edit'),
    path('add_comment/<int:pk>', views.add_comment, name= 'add_comment'),
    path('generate-post', views.creat_post, name= 'creat_post'),
    path('activate/<str:token>/',views.confirm_email, name='activate'),
    path('notifications/',views.notifications, name='notifications'),
    path('read/<int:notification_id>/',views.mark_notification_as_read, name='mark_notification_as_read'),

]





