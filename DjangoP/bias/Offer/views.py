from django.shortcuts import render, redirect
from .models import *
from .forms import *


def createOffer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.save()
            return redirect('drafts')
        
    else:
        form = OfferForm()

    return render(request, 'create_offer.html', {'form': form})


def drafts(request):
    offers = Offer.objects.filter()

    return render(request, 'drafts.html', {'offers': offers})