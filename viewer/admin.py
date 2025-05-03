from django.contrib import admin
from django.contrib.admin import ModelAdmin

from viewer.models import *


class AuthorAdmin(ModelAdmin):

    ordering = ['surname']
    list_display = ['id', 'surname', 'name', 'date_of_birth', 'date_of_death']
    list_display_links = ['surname']
    list_per_page = 10
    list_filter = ['nationality']
    search_fields = ['surname']



class BookAdmin(ModelAdmin):

    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)

    ordering = ['title_cz', 'year_of_publishing']
    list_display = ['id', 'title_cz', 'title_orig', 'year_of_publishing']
    list_display_links = ['id', 'title_cz', 'title_orig']
    list_per_page = 10
    list_filter = ['genre']
    search_fields = ['title_cz', 'title_orig']
    actions = ['cleanup_description']


    fieldsets = [
        ('Titles',
         {
             'fields': [
                 'title_cz',
                 'title_orig',
             ],
             'description': 'Název knihy [český a originální]'
         }),
        ('External information',
         {
             'fields': [
                 'genre',
                 'year_of_publishing',
                 'num_of_pages',
                 'time_of_reading',
                 'format',
             ]
         }),
        ('Authors',
         {
             'fields': [
                 'author'
             ]
         }),
        ('Publishers',
         {
             'fields': [
                 'publisher'
             ]
         }),
        ('User information',
         {
             'fields': [
                 'description',
                 'rating_ours',
                 'review'
             ]
         }),
        ('Internal information',
         {
             'fields': [
                 'created',
                 'updated'
             ]
         })

    ]
    readonly_fields = ['created', 'updated']

admin.site.register(Genre)
admin.site.register(Nationality)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Format)
admin.site.register(Publisher)
admin.site.register(Book, BookAdmin)
admin.site.register(Award)


