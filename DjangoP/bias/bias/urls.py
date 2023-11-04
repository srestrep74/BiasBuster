from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', analyze, name='analyze'),
    path('informs_diagrams/', informs_diagrams, name='informs_diagrams'),
    path('ubication/', ubication, name='ubication'),
    path('', include('Offer.urls')),
    path('', include('Analytics.urls'))
]
