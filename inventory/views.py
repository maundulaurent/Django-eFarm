from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product

def product_list(request):
    products = Product.objects.filter(is_available=True)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filter by product type
    product_type = request.GET.get('type')
    if product_type:
        products = products.filter(product_type=product_type)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    categories = Category.objects.all()
    
    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories,
        'product_types': Product.PRODUCT_TYPES,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(pk=pk)[:4]
    
    return render(request, 'inventory/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

@login_required
def add_product(request):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Only farmers can add products!')
        return redirect('product-list')
    
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        product_type = request.POST.get('product_type')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit')
        image = request.FILES.get('image')
        
        product = Product.objects.create(
            name=name,
            category_id=category_id,
            product_type=product_type,
            description=description,
            price=price,
            quantity=quantity,
            unit=unit,
            image=image
        )
        
        messages.success(request, f'{product.name} added successfully!')
        return redirect('product-detail', pk=product.pk)
    
    categories = Category.objects.all()
    return render(request, 'inventory/add_product.html', {
        'categories': categories,
        'product_types': Product.PRODUCT_TYPES
    })

@login_required
def update_product(request, pk):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Permission denied!')
        return redirect('product-list')
    
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.product_type = request.POST.get('product_type')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.unit = request.POST.get('unit')
        product.is_available = request.POST.get('is_available') == 'on'
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        
        product.save()
        messages.success(request, f'{product.name} updated successfully!')
        return redirect('product-detail', pk=product.pk)
    
    categories = Category.objects.all()
    return render(request, 'inventory/update_product.html', {
        'product': product,
        'categories': categories,
        'product_types': Product.PRODUCT_TYPES
    })

@login_required
def delete_product(request, pk):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Permission denied!')
        return redirect('product-list')
    
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, f'{product.name} deleted successfully!')
        return redirect('product-list')
    
    return render(request, 'inventory/delete_product.html', {'product': product})