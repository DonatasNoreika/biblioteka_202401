from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
from tinymce.models import HTMLField


# Create your models here.
class Genre(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=200,
                            help_text='Įveskite knygos žanrą (pvz. detektyvas)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = 'Žanrai'


class Author(models.Model):
    first_name = models.CharField(verbose_name='Vardas', max_length=100)
    last_name = models.CharField(verbose_name='Pavardė', max_length=100)
    description = HTMLField(verbose_name="Aprašymas", max_length=3000, default="")

    def display_books(self):
        return ", ".join(book.title for book in self.books.all())

    display_books.short_description = 'Knygos'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Autorius"
        verbose_name_plural = 'Autoriai'


class Book(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=200)
    author = models.ForeignKey(to="Author", verbose_name="Autorius", on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='books')
    summary = models.TextField(verbose_name="Aprašymas", max_length=1000, help_text='Trumpas knygos aprašymas')
    isbn = models.CharField(verbose_name="ISBN", max_length=13,
                            help_text='13 Simbolių <a href="https://www.isbn-international.org/content/what-isbn">ISBN kodas</a>')
    genre = models.ManyToManyField(to="Genre", verbose_name="Žanrai", help_text='Išrinkite žanrą(us) šiai knygai')
    cover = models.ImageField(verbose_name="Viršelis", upload_to="covers", null=True, blank=True)

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())

    display_genre.short_description = 'Žanras (-ai)'

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Knyga"
        verbose_name_plural = 'Knygos'


class BookInstance(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, help_text='Unikalus ID knygos kopijai')
    book = models.ForeignKey(to="Book", verbose_name="Knyga", on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="instances")
    due_back = models.DateField(verbose_name="Bus prieinama", null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="a", help_text='Statusas')
    reader = models.ForeignKey(to=User, verbose_name="Skaitytojas", on_delete=models.SET_NULL, null=True, blank=True)

    def is_overdue(self):
        return self.due_back and datetime.date.today() > self.due_back

    def __str__(self):
        return f"{self.uuid} ({self.book.title}) - {self.get_status_display()} - {self.due_back})"

    class Meta:
        ordering = ('due_back',)
        verbose_name = "Knygos egzempliorius"
        verbose_name_plural = 'Knygos egzemplioriai'
