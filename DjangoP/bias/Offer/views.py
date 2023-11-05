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
            offer.save()
            id = offer.id
            prompt(id)
            return redirect('drafts')
        
    else:
        form = OfferForm()

    return render(request, 'create_offer.html', {'form': form})


def drafts(request):
    offers = Offer.objects.filter()

    return render(request, 'drafts.html', {'offers': offers})


def prompt(offer_id):
    offer = Offer.objects.get(pk=offer_id)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Eres una maquina analista de ofertas laborales, que se basa en el analisis del discurso. Unicamente detectas racismo, sexismo, xenofobia y edad, no otros sesgos. Siempre das tres respuestas, exactas y precisas. Respondes primero con cuatro numeros, que corresponden a cada tipo de sesgo respectivamente (Cada numero va a ser dado por la cantidad de oraciones con ese sesgo en la oferta que encuentres). Luego escribes exactamente la oración de la oferta donde detectaste el sesgo. Luego das una redacción completa de la oferta eliminando el sesgo, si es que existe alguna oración con sesgo, si todo esta sin sesgo, devuelves la oferta tal cual ingreso. Eres muy inclusivo en todos los sentidos, te gusta incluir a todas las personas. Tu formato como maquina es el siguiente: xyzk // o1--o2--...--on // tr. Donde x,y,z,k son los numeros del inicio. o1--o2--,...,--on son las oraciones con sesgo y tr es el texto corregido. Debes seguir ese formato al pie de la letra, reemplazando cada simbolo segun lo que analices."},
            {"role": "user", "content": f"Realiza el analisis para la siguiente oferta: {offer.description}"}
        ]
    )

    result = completion.choices[0].message["content"]
    print(result)

    parts = result.split(" // ")
    if len(parts) == 3:
        xyzk, highlight_words, corrected_description = parts
    else:
        xyzk, highlight_words, corrected_description = "", "", result

    if int(xyzk[0]) > 0:
        offer.bias.add(Bias.objects.get(pk=1))
    if int(xyzk[1]) > 0:
        offer.bias.add(Bias.objects.get(pk=2))
    if int(xyzk[2]) > 0:
        offer.bias.add(Bias.objects.get(pk=3))
    if int(xyzk[3]) > 0:
        offer.bias.add(Bias.objects.get(pk=4))
    
    suggestion = Suggestion(
        corrected_description=corrected_description,
        highlight_words=highlight_words,
        offer=offer
    )
    suggestion.save()


def bias(request, id):
    offer = Offer.objects.get(pk=id)
    suggestion = Suggestion.objects.get(offer=offer)
    context = {
        'offer': offer,
        'suggestion': suggestion
    }

    return render(request, 'bias.html', context)