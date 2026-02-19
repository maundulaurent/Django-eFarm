# services/admin.py
from django.contrib import admin
from .models import Service, ServiceBooking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'price', 'duration', 'is_available']
    list_filter = ['service_type', 'is_available']
    search_fields = ['title', 'description']
    list_editable = ['price', 'is_available']
    
    fieldsets = (
        ('Service Details', {
            'fields': ('title', 'service_type', 'description')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration', 'is_available')
        })
    )

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ['service', 'customer', 'booking_date', 'is_confirmed', 'created_at']
    list_filter = ['is_confirmed', 'booking_date', 'service']
    search_fields = ['customer__username', 'customer__email', 'service__title']
    list_editable = ['is_confirmed']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('service', 'customer', 'booking_date')
        }),
        ('Additional Details', {
            'fields': ('notes', 'is_confirmed')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )