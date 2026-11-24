from django.contrib import admin
from .models import Serie


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'rating', 'release_date')
    list_filter = ('category', 'rating')
    search_fields = ('name',)
