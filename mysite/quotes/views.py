from django.shortcuts import get_object_or_404, render
from .models import Faculties, Professors, Quotes
from django.db.models import Count
from django.http import JsonResponse

def main(request):
    quotes = Quotes.objects.all()[:9]
    return render(request, 'quotes/some.html', {'quotes': quotes})

def facs(request):
    faculties = Faculties.objects.annotate(quotes_count=Count('professors__quotes'))
    quotes = Quotes.objects.all()
    return render(request, 'quotes/faculties.html', {'faculties': faculties, 'quotes': quotes})

def faculty_detail(request, slug):
    faculty = Faculties.objects.get(slug=slug)
    quotes = Quotes.objects.filter(professor__faculty=faculty)
    return render(request, 'quotes/faculties_detail.html', {'faculty': faculty, 'quotes': quotes})

def  popular_quotes(request):
    quotes = Quotes.objects.order_by('-likes_count')[:20]
    return render(request, 'quotes/top_popular.html', {'quotes': quotes})

def about_us(request):
    return render(request, 'quotes/about_us.html', {})

def profs(request):
    professors = Professors.objects.all()
    return render(request, 'quotes/professors.html', {'professors': professors})

def professor_detail(request, slug):
    professor = Professors.objects.get(slug=slug)
    quotes = Quotes.objects.filter(professor=professor)
    return render(request, 'quotes/professors_detail.html', {'professor': professor, 'quotes': quotes})

def search_professors(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        professors = Professors.objects.filter(name__icontains=query)[:10]
        results = [{'name': prof.name, 'slug': prof.slug} for prof in professors]
    return JsonResponse(results, safe=False)

def search_faculties(request):
    query = request.GET.get('q', '')
    results = Faculties.objects.filter(name__icontains=query).values('name', 'slug')[:10]
    return JsonResponse(list(results), safe=False)