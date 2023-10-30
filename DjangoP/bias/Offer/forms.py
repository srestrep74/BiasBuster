from django import forms
from .models import *


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('title', 'description', 'salary', 'sectors', 'key_words', 
                  'study_level', 'charge', 'location')