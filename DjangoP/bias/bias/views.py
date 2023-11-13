from django.shortcuts import render


def analyze(request):
    return render(request, 'analyze.html')

def informs_diagrams(request):
    company = request.user.company.id 
    return render(request, 'informs_diagrams.html' , {'company_id' : company})


def ubication(request):
    return render(request, 'ubication.html')