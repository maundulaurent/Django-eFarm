from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import JsonResponse
from .models import Order, OrderItem
from inventory.models import Product

@login_required
def order_list(request):
    if request.user.user_type == 'FARMER':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(customer=request.user)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    return render(request, 'sales/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'sales/order_detail.html', {'order': order})

@login_required
def create_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('product-list')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            customer=request.user,
            order_number=f"ORD-{request.user.id}-{Order.objects.count() + 1:06d}",
            total_amount=request.POST.get('total_amount'),
            shipping_address=request.POST.get('shipping_address'),
            notes=request.POST.get('notes', '')
        )
        
        # Create order items
        for product_id, item_data in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=product.price
            )
        
        # Clear cart
        request.session['cart'] = {}
        messages.success(request, f'Order {order.order_number} created successfully!')
        return redirect('order-detail', order_number=order.order_number)
    
    # Calculate total
    total = 0
    cart_items = []
    for product_id, item_data in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * item_data['quantity']
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity'],
            'subtotal': subtotal
        })
    
    return render(request, 'sales/create_order.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def update_order_status(request, order_number):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Permission denied!')
        return redirect('order-list')
    
    order = get_object_or_404(Order, order_number=order_number)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, f'Order status updated to {new_status}')
    
    return redirect('order-detail', order_number=order_number)

def cart_view(request):
    cart = request.session.get('cart', {})
    total = 0
    cart_items = []
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * item_data['quantity']
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue
    
    return render(request, 'sales/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'quantity': 1,
            'name': product.name,
            'price': str(product.price)
        }
    
    request.session['cart'] = cart
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'cart_count': len(cart), 'message': 'Added to cart!'})
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('product-list')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart!')
    
    return redirect('cart-view')