from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Service, ServiceBooking

def service_list(request):
    services = Service.objects.filter(is_available=True)
    
    # Filter by service type
    service_type = request.GET.get('type')
    if service_type:
        services = services.filter(service_type=service_type)
    
    # Search
    query = request.GET.get('q')
    if query:
        services = services.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    return render(request, 'services/service_list.html', {
        'services': services,
        'service_type': service_type,
        'query': query
    })

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})

@login_required
def book_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        booking = ServiceBooking.objects.create(
            customer=request.user,
            service=service,
            booking_date=request.POST.get('booking_date'),
            notes=request.POST.get('notes', ''),
            is_confirmed=False
        )
        messages.success(request, f'Booking request sent for {service.title}! We\'ll confirm shortly.')
        return redirect('service-detail', pk=service.pk)
    
    return render(request, 'services/book_service.html', {'service': service})

@login_required
def my_bookings(request):
    bookings = ServiceBooking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'services/my_bookings.html', {'bookings': bookings})

@login_required
def manage_bookings(request):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Permission denied!')
        return redirect('service-list')
    
    bookings = ServiceBooking.objects.all().order_by('-created_at')
    return render(request, 'services/manage_bookings.html', {'bookings': bookings})

@login_required
def confirm_booking(request, booking_id):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Permission denied!')
        return redirect('service-list')
    
    booking = get_object_or_404(ServiceBooking, id=booking_id)
    booking.is_confirmed = True
    booking.save()
    messages.success(request, f'Booking for {booking.customer.username} confirmed!')
    
    return redirect('manage-bookings')