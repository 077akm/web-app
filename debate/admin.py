from django.contrib import admin

from .models import *

class DebateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'image', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Debate, DebateAdmin)
admin.site.register(Category, CategoryAdmin)
