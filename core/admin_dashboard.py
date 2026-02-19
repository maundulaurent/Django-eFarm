# admin_dashboard.py or add to any app's admin.py
from django.contrib import admin
from django.db.models import Sum, Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta

class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_list = super().get_app_list(request)
        
        # Add custom dashboard summary
        from inventory.models import Product
        from livestock.models import Livestock
        from sales.models import Order
        from blog.models import Article
        
        # Calculate statistics for the dashboard
        context = {
            'total_products': Product.objects.count(),
            'available_products': Product.objects.filter(is_available=True).count(),
            'total_livestock': Livestock.objects.count(),
            'healthy_livestock': Livestock.objects.filter(status='HEALTHY').count(),
            'pending_orders': Order.objects.filter(status='PENDING').count(),
            'total_orders': Order.objects.count(),
            'published_articles': Article.objects.filter(is_published=True).count(),
        }
        
        # Add context to request for use in admin templates
        request.admin_stats = context
        
        return app_list

# To use this custom admin site, add to your apps' admin.py:
# admin_site = CustomAdminSite(name='custom_admin')