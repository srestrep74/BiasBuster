from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login, name='login'),
    path('prueba', prueba, name='prueba'),
    path('logout/', logoutAccount, name='logout'),
]