# livestock/admin.py
from django.contrib import admin
from .models import AnimalType, Livestock

@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Livestock)
class LivestockAdmin(admin.ModelAdmin):
    list_display = ['tag_number', 'animal_type', 'breed', 'gender', 'date_of_birth', 'status', 'weight']
    list_filter = ['animal_type', 'breed', 'gender', 'status', 'date_added']
    search_fields = ['tag_number', 'breed', 'notes']
    list_editable = ['status', 'weight']
    readonly_fields = ['date_added']
    
    fieldsets = (
        ('Identification', {
            'fields': ('animal_type', 'breed', 'tag_number', 'gender')
        }),
        ('Health & Status', {
            'fields': ('date_of_birth', 'status', 'weight', 'notes')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('date_added',)
        })
    )
    
    def age_display(self, obj):
        from datetime import date
        if obj.date_of_birth:
            age = date.today() - obj.date_of_birth
            return f"{age.days} days"
        return "Unknown"
    age_display.short_description = 'Age'