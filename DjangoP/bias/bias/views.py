from django.shortcuts import render


def analyze(request):
    return render(request, 'analyze.html')

def informs_diagrams(request):
    return render(request, 'informs_diagrams.html')


def ubication(request):
    return render(request, 'ubication.html')