from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User, auth
from Offer.models import *
from django.db.models import Count , F


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username , password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('drafts')
        else:
            messages.info(request, 'Usuario o contraseña son incorrectos')
            return redirect('login')
        
    return render(request, 'login.html')

def graph_contains_bias(company_id):
    company =  Company.objects.get(id=company_id)
    offers_total = Offer.objects.filter(company=company).count()
    offers_bias = Offer.filter(company=company, bias__isnull=False).distinct().count()

    return  offers_total, offers_total

def graph_by_bias(company_id):
    company  = Company.objects.get(id=company_id)
    offerts_total = Offer.objects.filter(company=company_id).count()
    bias_percentage = Bias.objects.annotate(
        quantity_bias = Count('offer__bias', filter=F('offer__company')== company)
    ).values('type', 'quantity_bias', percentage=F('bias_percentage')*100/offerts_total)

    return bias_percentage

def prueba(request, company_id):
    offers_total , offers_bias = graph_contains_bias(company_id)

    bias_percentage = graph_by_bias(company_id)

    context= {
        'offers_total' : offers_total,
        'offers_bias' : offers_bias,
        'bias_percentage' : bias_percentage
    }



    return render(request, 'analisis.html', context)

