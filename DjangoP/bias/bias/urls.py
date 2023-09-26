from django.contrib import admin
from django.urls import path
from .views import analyze, drafts, bias, informs_diagrams, ubication

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze/', analyze, name='analyze'),
    path('drafts/', drafts, name='drafts'),
    path('bias/', bias, name='bias'),
    path('informs_diagrams/', informs_diagrams, name='informs_diagrams'),
    path('ubication/', ubication, name='ubication')
]
