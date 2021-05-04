from django.contrib import admin
from. import models


#admin.site.register(models.Material)
@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'create_date')
    list_filter = ('create_date', 'text')
    search_fields = ('name', 'text')