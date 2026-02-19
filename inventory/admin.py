# inventory/admin.py
from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']} if hasattr(Category, 'slug') else {}
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'product_type', 'price', 'quantity', 'unit', 'is_available', 'created_at']
    list_filter = ['product_type', 'category', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'quantity', 'is_available']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'product_type', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'quantity', 'unit', 'is_available')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )