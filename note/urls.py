from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path('login', loginPage, name="login"),
    path('register', registerPage, name="register"),
    path('forgot', forgotPage, name="forgot"),
    path('updatePassword', update_Password, name="updatePassword"),
    path('logout', logoutPage, name="logout"),
    path('<int:id>', delnote)
]
