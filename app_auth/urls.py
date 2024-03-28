from django.urls import path
from .views import *

urlpatterns = [
    path('login',login_blog,name='login-blog'),
    path('register',register,name='register'),
    path('logout',logout_blog,name='logout'),
    path('confirm-registration/<uidb64>/<token>/', confirm_registration, name='confirm-registration'),
]