from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login, name='login'),
    path('prueba/<int:id>/<str:date_filter>', prueba, name='prueba'),
    path('logout/', logoutAccount, name='logout'),
   
]