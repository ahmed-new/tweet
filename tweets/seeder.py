from .models import Post
from django.contrib.auth.models import User
import random
from faker import Faker

def run():
    faker = Faker()

    # إضافة المستخدمين
    for _ in range(20):
        User.objects.create_user(username=faker.user_name(), email=faker.email(), password='password')

    users = User.objects.all()

    # إضافة المنشورات
    for _ in range(80):
        Post.objects.create(user=random.choice(users), body=faker.text(max_nb_chars=200), created=faker.date_time_this_year())
