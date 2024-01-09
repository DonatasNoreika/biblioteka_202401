from django.contrib import admin
from .models import Genre, Book, Author, BookInstance


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'display_genre']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'status', 'due_back']
    list_filter = ['status', 'due_back']

    fieldsets = (
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'due_back')}),
    )

# Register your models here.
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
