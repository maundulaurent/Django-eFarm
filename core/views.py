from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from inventory.models import Product, Category
from livestock.models import Livestock
from sales.models import Order
from blog.models import Article
from services.models import Service
from services.models import ServiceBooking

def home(request):
    inventory_category = Category.objects.order_by('?').first()
    recent_products = Product.objects.filter(is_available=True)[:6]
    recent_articles = Article.objects.filter(is_published=True)[:3]
    services = Service.objects.filter(is_available=True)[:4]
    
    context = {
        'inventory_category' : inventory_category,
        'recent_products': recent_products,
        'recent_articles': recent_articles,
        'services': services,
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard(request):
    # General stats
    context = {
        'total_products': Product.objects.count(),
        'available_products': Product.objects.filter(is_available=True).count(),
        'total_livestock': Livestock.objects.count(),
        'healthy_livestock': Livestock.objects.filter(status='HEALTHY').count(),
        'total_articles': Article.objects.filter(is_published=True).count(),
    }
    
    # Farmer-specific stats
    if request.user.user_type == 'FARMER':
        # Sales stats
        last_7_days = timezone.now() - timedelta(days=7)
        recent_orders = Order.objects.filter(created_at__gte=last_7_days)
        
        context.update({
            'recent_orders': recent_orders[:10],
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(status='PENDING').count(),
            'total_revenue': Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'pending_bookings': ServiceBooking.objects.filter(is_confirmed=False).count(),
            'recent_bookings': ServiceBooking.objects.order_by('-created_at')[:5],
        })
    
    # Customer-specific stats
    elif request.user.user_type == 'CUSTOMER':
        context.update({
            'my_orders': Order.objects.filter(customer=request.user).count(),
            'my_bookings': ServiceBooking.objects.filter(customer=request.user).count(),
        })
    
    return render(request, 'core/dashboard.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')