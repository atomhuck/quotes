from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Faculties, Professors, Quotes, QuotesProfessors

def main(request):
    quotes = Quotes.objects.all()[:9]
    return render(request, 'quotes/some.html', {'quotes': quotes})

def facs(request):
    faculties = Faculties.objects.all()
    return render(request, 'quotes/faculties.html', {'faculties': faculties})

def faculty_detail(request, slug):
    faculty = Faculties.objects.get(slug=slug)
    quotes = Quotes.objects.filter(professor__faculty=faculty)
    return render(request, 'quotes/faculties_detail.html', {'faculty': faculty, 'quotes': quotes})

def  popular_quotes(request):
    quotes = Quotes.objects.order_by('-likes_count')[:20]
    return render(request, 'quotes/top_popular.html', {'quotes': quotes})

def about_us(request):
    return render(request, 'quotes/about_us.html', {})