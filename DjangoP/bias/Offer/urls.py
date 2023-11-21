from django.urls import path
from .views import *


urlpatterns = [
    path('create_offer/', createOffer, name='create_offer'),
    path('drafts/', drafts, name='drafts'),
    path('bias/<int:id>', bias, name='bias'),
    path('replace_description/<int:id>', replaceOffer, name='replace'),
    path('', analyze, name='analyze'),
    path('informs_diagrams/', informs_diagrams, name='informs_diagrams')
]