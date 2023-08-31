from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from store.views import createBox , getAllBoxes , getUserBox , updateBox , deleteBox , userRegistration
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('box/create/' , createBox , name="createBox"),
    path('box/all-box/' , getAllBoxes , name="getAllBoxes"),
    path('box/user-box/' , getUserBox , name="getUserBox"),
    path('box/update/<int:pk>', updateBox,name='updateBox'),
    path('box/delete/<int:pk>', deleteBox,name='deleteBox'),
    path('register/', userRegistration, name='userRegistration'),
    path('login/', obtain_auth_token, name='login')
]
