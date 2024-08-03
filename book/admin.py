from django.contrib import admin

from book.models import Book


# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price')
    search_fields = ('name', 'author')
