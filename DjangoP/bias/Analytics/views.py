from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User, auth
from Offer.models import *
from django.db.models import Count , F, Value
from django.contrib.auth import login, logout, authenticate
from datetime import datetime, timedelta


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


def logoutAccount(request):
    logout(request)
    return redirect('login')




def graph_contains_bias(company_id, date_filter):
    company =  Company.objects.get(id=company_id)

    today = datetime.now().date()

    offers_total = None

    if date_filter == 'today':
        offers_total = Offer.objects.filter(company=company,date=today).count()
    elif date_filter == 'yesterday':
        yesterday = today-timedelta(days=1)
        offers_total = Offer.objects.filter(company=company, date=yesterday).count()
    elif date_filter == 'last_7_days':
        seven_days_ago = today-timedelta(days=7)
        offers_total = Offer.objects.filter(company=company,date__gte=seven_days_ago).count()
    else : 
        month = today-timedelta(days=30)
        offers_total = Offer.objects.filter(company=company,date__gte=month).count()

    offers_bias = Offer.objects.filter(company=company, bias__isnull=False).distinct().count()

    return offers_total, offers_bias


def graph_by_bias(company_id, date_filter):
    company  = Company.objects.get(id=company_id)

    today = datetime.now().date()
    offers_queryset = None
    if date_filter == 'today':
        offers_queryset = Offer.objects.filter(company=company, date=today)
    elif date_filter == 'yesterday':
        offers_queryset = Offer.objects.filter(company=company, date=today-timedelta(days=1))
    elif date_filter == 'last_7_days':
        offers_queryset = Offer.objects.filter(company=company, date__gte=today-timedelta(days=7))
    elif date_filter == 'month':
        offers_queryset = Offer.objects.filter(company=company, date__gte=today-timedelta(days=30))
    offerts_total = offers_queryset.count()

    bias_percentage = Bias.objects.filter(offer__in=offers_queryset).annotate(
        quantity_bias=Count('offer__bias'),
        percentage=F('quantity_bias') * 100 / Value(offerts_total, output_field=models.FloatField())
    ).values('type', 'quantity_bias', 'percentage')

    return bias_percentage

def format_bias(company_id, date_filter):
    bias_percentage = graph_by_bias(company_id, date_filter)
    res = {
        "Sexismo" : 0,
        "Racismo" : 0 ,
        "Ubicacion" : 0,
        "Ideologias" : 0,
        "Edad" : 0,
        "Xenofobia" : 0,
        "Ninguno" : 0,
    }
    for bias in bias_percentage:
        res[bias['type']] = bias['quantity_bias'] 
    return res



def prueba(request, id, date_filter):
    year_bias_general, year_bias_specific,sexismo,racismo, ubicacion, ideologias, edad, xenofobia, ninguno = bias_by_time(id)
    offers_total, offers_bias = graph_contains_bias(id, date_filter)
    bias_percentage = format_bias(id, date_filter)

    print(type(sexismo), sexismo)

    bias_last = bias_last_year(id)


    types = {
        'sexismo' : sexismo,
        'racismo' : racismo,
        'ubicacion' : ubicacion,
        'ideologias' : ideologias,
        'edad' : edad,
        'xenofobia' : xenofobia,
        'ninguno' : ninguno
    }

    f = 0
    total_bias = 0
    for b,q in bias_percentage.items():
        if  q > 0 :
            f = 1
        total_bias += q
    if f == 0:
        bias_percentage['Ninguno'] = 100
    
    act, last = bar_comparative_format(id)

    print(year_bias_specific[1])

    context= {
        'offers_total' : offers_total,
        'offers_bias' : offers_bias,
        'bias_percentage' : bias_percentage,
        'total_bias' : total_bias,
        'act' : act,
        'last' : last,

        #Miguel
        'spe_jan' : year_bias_specific[0],
        'spe_feb' : year_bias_specific[1],
        'spe_marc' : year_bias_specific[2],
        'spe_apr' : year_bias_specific[3],
        'spe_may' : year_bias_specific[4],
        'spe_jun' : year_bias_specific[5],
        'spe_jul' : year_bias_specific[6],
        'spe_aug' : year_bias_specific[7],
        'spe_sep' : year_bias_specific[8],
        'spe_oct' : year_bias_specific[9],
        'spe_nov' : year_bias_specific[10],
        'spe_dec' : year_bias_specific[11],
        'types' : types,
        'last_year' : bias_last,
        'time_general' : year_bias_general,
        
    }

    

    return render(request, 'analisis.html', context)

def bar_comparative(company_id):
    company  = Company.objects.get(id=company_id)
    today = datetime.now().date()
    offers_queryset = Offer.objects.filter(company=company, date__gte=today-timedelta(days=30))
    offerts_total = offers_queryset.count()
    actual = Bias.objects.filter(offer__in=offers_queryset).annotate(
        quantity_bias=Count('offer__bias'),
        percentage=F('quantity_bias') * 100 / Value(offerts_total, output_field=models.FloatField())
    ).values('type', 'quantity_bias', 'percentage')

    offers_queryset = Offer.objects.filter(company=company, date__lte=today-timedelta(days=60))

    offerts_total = offers_queryset.count()
    last = Bias.objects.filter(offer__in=offers_queryset).annotate(
        quantity_bias=Count('offer__bias'),
        percentage=F('quantity_bias') * 100 / Value(offerts_total, output_field=models.FloatField())
    ).values('type', 'quantity_bias', 'percentage')

    return actual, last

def bar_comparative_format(company_id):
    actual ,  last = bar_comparative(company_id)
    resact = {
        "Sexismo" : 0,
        "Racismo" : 0 ,
        "Ubicacion" :0,
        "Ideologias" : 0,
        "Edad" : 0,
        "Xenofobia" :0,
    }
    resla = {
        "Sexismo" : 0,
        "Racismo" : 0 ,
        "Ubicacion" :0,
        "Ideologias" : 0,
        "Edad" : 0,
        "Xenofobia" :0,
    }
    for bias in actual:
        resact[bias['type']] = bias['quantity_bias'] 
    for bias in last:
        resla[bias['type']] = bias['quantity_bias'] 
    return resact, resla

def bias_by_time(company_id):
    bias_by_month_specific = [0]*12
    sexismo = [0]*12
    racismo = [0]*12
    ubicacion = [0]*12
    ideologias = [0]*12
    edad = [0]*12
    xenofobia = [0]*12
    ninguno = [0]*12 
    i = 0
    while i < 12:
        res = {
            "Sexismo" : 0,
            "Racismo" : 0 ,
            "Ubicacion" : 0,
            "Ideologias" : 0,
            "Edad" : 0,
            "Xenofobia" : 0,
            "Ninguno" : 0,
        }
        bias_by_month_specific[i] = res
        i+=1


    bias_by_month_general = [0]*12
    company = Company.objects.get(id=company_id) 
    today = datetime.now().date()
    year=today.year
    start_time = datetime(year=year, month=1, day = 1)
    end_time = datetime(year=year, month=12, day=31)
    offers_queryset = Offer.objects.filter(company=company, date__gte = start_time, date__lt=end_time)
    for offer in offers_queryset:
        bias_by_month_general[offer.date.month-1] += 1
        bias_offer = [bias.type for bias in offer.bias.all()]
        for type_bias in bias_offer:
            bias_by_month_specific[offer.date.month-1][type_bias]+=1
            if type_bias == "Sexismo":
                sexismo[offer.date.month-1] += 1
            elif type_bias == "Racismo":
                racismo[offer.date.month-1] += 1
            elif type_bias == "Ubicacion":
                ubicacion[offer.date.month-1] += 1
            elif type_bias == "Ideologias":
                ideologias[offer.date.month-1] += 1
            elif type_bias == "Edad":
                edad[offer.date.month-1] += 1
            elif type_bias == "Xenofobia":
                xenofobia[offer.date.month-1] += 1
            elif type_bias == "Ninguno":
                ninguno[offer.date.month-1] += 1
    
    return bias_by_month_general, bias_by_month_specific, sexismo, racismo, ubicacion, ideologias, edad, xenofobia, ninguno

def bias_last_year(company_id):
    bias_by_year = [0]*12
    company = Company.objects.get(id=company_id) 
    today = datetime.now().date()
    year=today.year
    start_time = datetime(year=year-1, month=1, day = 1)
    end_time = datetime(year=year-1, month=12, day=31)
    offers_queryset = Offer.objects.filter(company=company, date__gte = start_time, date__lt=end_time)
    for offer in offers_queryset:
        bias_by_year[offer.date.month-1] += 1
    return bias_by_year



