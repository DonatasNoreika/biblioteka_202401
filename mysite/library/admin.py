from django.contrib import admin
from .models import Genre, Book, Author, BookInstance, BookReview, Profile


class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0
    can_delete = False
    readonly_fields = ['uuid']


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'display_genre']
    inlines = [BookInstanceInLine]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'status', 'due_back', 'reader']
    list_filter = ['status', 'due_back']
    search_fields = ['uuid', 'book__title']
    list_editable = ['due_back', 'status', 'reader']

    fieldsets = (
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'due_back', 'reader')}),
    )


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'date_created', 'reviewer', 'content']

# Register your models here.
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(Profile)
