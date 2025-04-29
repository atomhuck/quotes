from django.db import models
from slugify import slugify


class Faculties(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Professors(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE, related_name="professors", blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Professors.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Quotes(models.Model):
    text = models.TextField(blank=True, null=True)
    professor = models.ForeignKey(Professors, on_delete=models.CASCADE, related_name="quotes", blank=True, null=True)
    likes_count = models.PositiveIntegerField(default=0)
    reposts_count = models.PositiveIntegerField(default=0)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.text[:50]}..." if self.text else "No text"


class QuotesProfessorRaw(models.Model):
    quote_text = models.TextField(blank=True, null=True)
    professor_name = models.CharField(max_length=255, blank=True, null=True)
    faculty_name = models.CharField(max_length=255, blank=True, null=True)
    faculty_ref = models.ForeignKey(Faculties, on_delete=models.SET_NULL, db_column='faculty_id', blank=True, null=True)

    class Meta:
        db_table = 'quotes_professors_raw'

    def __str__(self):
        return self.quote_text[:50] if self.quote_text else "Raw quote"