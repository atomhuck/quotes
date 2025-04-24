from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Faculties, Professors, Quotes, QuotesProfessors

def main(request):
    quotes = Quotes.objects.all()[:9]
    return render(request, 'quotes/some.html', {'quotes': quotes})

def facs(request):
    faculties = Faculties.objects.all()[:20]
    return render(request, 'quotes/faculties.html', {'faculties': faculties})