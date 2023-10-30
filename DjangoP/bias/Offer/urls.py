from django.urls import path
from .views import *


urlpatterns = [
    path('create_offer/', createOffer, name='create_offer'),
]