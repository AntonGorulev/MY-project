from django.contrib import admin
from. import models


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'create_date')
    list_filter = ('create_date', 'text')
    search_fields = ('name', 'text')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('birth', 'photo', 'user')
