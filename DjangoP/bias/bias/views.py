from django.shortcuts import render


def drafts(request):
    return render(request, 'drafts.html')


def analyze(request):
    return render(request, 'analyze.html')


def bias(request):
    return render(request, 'bias.html')


def informs_diagrams(request):
    return render(request, 'informs_diagrams.html')


def ubication(request):
    return render(request, 'ubication.html')