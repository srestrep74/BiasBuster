from django.shortcuts import render, redirect
from .models import *
from .forms import *
import openai
import environ


env = environ.Env()
environ.Env.read_env('../bias/')
openai.api_key = env('API')


def createOffer(request):
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            company = request.user
            offer.company = company.company
            offer.save()
            id = offer.id
            prompt(id)
            return redirect('drafts')
        
    else:
        form = OfferForm()

    return render(request, 'offer/create_offer.html', {'form': form})


def drafts(request):
    search_term = request.GET.get('searchOffer')
    company = request.user
    if search_term:
        offers = Offer.objects.filter(company = company.company, title__icontains=search_term)
    else:
        offers = Offer.objects.filter(company = company.company)

    return render(request, 'offer/drafts.html', {'offers': offers})


def prompt(offer_id):
    offer = Offer.objects.get(pk=offer_id)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {
                "role": "system", "content": "Eres una maquina analista de ofertas laborales, que se basa en el analisis del discurso. Unicamente detectas racismo, sexismo, xenofobia y homofobia, no otros sesgos. Siempre das tres respuestas, exactas y precisas. Respondes primero con un número según el sesgo que encontraste en la oferta y marcala con 1 (Incluye los 4 sesgos inclusive si este no aparece, si no aparece marcalo con 0). Luego escribes exactamente la oración de la oferta donde detectaste el sesgo. Luego das una redacción completa de la oferta eliminando el sesgo, si es que existe alguna oración con sesgo, si todo esta sin sesgo, devuelves la oferta tal cual ingreso. Eres muy inclusivo en todos los sentidos, te gusta incluir a todas las personas. Tu formato como maquina es el siguiente: xyzk // o1--o2--...--on // tr. Donde x,y,z,k son los cuatro números que representan los sesgos que aparecen en la oferta, siengo 'x' el número para racismo, 'y' el número para sexismo, 'z' el número para xenofobia y 'k' el número para homofobia. o1--o2--,...,--on son las oraciones con sesgo y tr es el texto corregido. Debes seguir ese formato al pie de la letra, reemplazando cada simbolo segun lo que analices. Ejemplos de oraciones con sesgo: - Racismo: La empresa prefiere candidatos de una determinada etnia. - Sexismo: Se busca un candidato masculino para liderar el equipo. - Xenofobia: Se dará preferencia a candidatos locales sobre extranjeros. - Homofobia: Buscamos a alguien que no pertenezca a ningún tipo de comunidad LGBTI etc. Un ejemplo de output por tu parte sería: R0S1X1H0 // No se permiten mujeres porque solo sirven para barrer y traperar. No se permiten extranjeros y mucho menos venezolanos. // Se busca a una persona para realizar tareas de limpieza y mantenimiento. Se valora la experiencia y el compromiso. Se aceptan candidatos de todas las nacionalidades."
            },
            {
                "role": "user", "content": f"Genera un analisis con el siguiente formato. Tu formato como maquina es el siguiente: xyzk // o1--o2--...--on // tr. Donde x,y,z,k son los cuatro números que representan los sesgos que aparecen en la oferta, siengo 'x' el número para racismo, 'y' el número para sexismo, 'z' el número para xenofobia y 'k' el número para homofobia. o1--o2--,...,--on son las oraciones con sesgo y tr es el texto corregido. Debes seguir ese formato al pie de la letra, reemplazando cada simbolo segun lo que analices. La oferta es: {offer.description}"
            }
        ]
    )

    result = completion.choices[0].message["content"]
    print(result)

    parts = result.split(" // ")
    if len(parts) == 3:
        xyzk, highlight_words, corrected_description = parts
    else:
        xyzk, highlight_words, corrected_description = "", "", result

    flag = False
    if int(xyzk[1]) > 0:
        offer.bias.add(Bias.objects.get(pk=1))
        flag = True
    if int(xyzk[3]) > 0:
        offer.bias.add(Bias.objects.get(pk=2))
        flag = True
    if int(xyzk[5]) > 0:
        offer.bias.add(Bias.objects.get(pk=3))
        flag = True

    if flag == False:
        offer.bias.add(Bias.objects.get(pk=7))
        offer.analyzed = 1
    
    suggestion = Suggestion(
        corrected_description=corrected_description,
        highlight_words=highlight_words,
        offer=offer
    )
    suggestion.save()


def bias(request, id):
    offer = Offer.objects.get(pk=id)
    suggestion = Suggestion.objects.get(offer=offer)
    q_offers = len([parte.strip() for parte in offer.description.split('.') if parte.strip()])
    q_suggest = len([parte.strip() for parte in suggestion.highlight_words.split('.') if parte.strip()])
    context = {
        'offer': offer,
        'suggestion': suggestion,
        'q_offers' : q_offers,
        'q_suggest' : q_suggest
        
    }

    return render(request, 'offer/bias.html', context)


def replaceOffer(request, id):
    offer = Offer.objects.get(pk=id)
    suggestion = Suggestion.objects.get(offer=offer)
    offer.description, suggestion.corrected_description = suggestion.corrected_description, offer.description
    offer.analyzed = 1
    offer.bias.clear()
    offer.bias.add(Bias.objects.get(pk=7))
    offer.save()

    return redirect('drafts')


def analyze(request):
    return render(request, 'graphics/analyze.html')


def informs_diagrams(request):
    company = request.user.company.id 
    return render(request, 'graphics/informs_diagrams.html' , {'company_id': company})