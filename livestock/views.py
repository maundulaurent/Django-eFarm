from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import AnimalType, Livestock

def livestock_list(request):
    animals = Livestock.objects.all()
    
    # Filter by animal type
    animal_type_id = request.GET.get('type')
    if animal_type_id:
        animals = animals.filter(animal_type_id=animal_type_id)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        animals = animals.filter(status=status)
    
    # Search
    query = request.GET.get('q')
    if query:
        animals = animals.filter(
            Q(breed__icontains=query) |
            Q(tag_number__icontains=query) |
            Q(notes__icontains=query)
        )
    
    animal_types = AnimalType.objects.all()
    status_choices = Livestock._meta.get_field('status').choices
    
    return render(request, 'livestock/livestock_list.html', {
        'animals': animals,
        'animal_types': animal_types,
        'status_choices': status_choices,
    })

def livestock_detail(request, pk):
    animal = get_object_or_404(Livestock, pk=pk)
    return render(request, 'livestock/livestock_detail.html', {'animal': animal})

@login_required
def add_livestock(request):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Only farmers can add livestock!')
        return redirect('livestock-list')
    
    if request.method == 'POST':
        animal = Livestock.objects.create(
            animal_type_id=request.POST.get('animal_type'),
            breed=request.POST.get('breed'),
            tag_number=request.POST.get('tag_number'),
            date_of_birth=request.POST.get('date_of_birth'),
            gender=request.POST.get('gender'),
            weight=request.POST.get('weight') or None,
            notes=request.POST.get('notes', '')
        )
        
        if request.FILES.get('image'):
            animal.image = request.FILES.get('image')
            animal.save()
        
        messages.success(request, f'Livestock added with tag: {animal.tag_number}')
        return redirect('livestock-detail', pk=animal.pk)
    
    animal_types = AnimalType.objects.all()
    return render(request, 'livestock/add_livestock.html', {
        'animal_types': animal_types
    })

@login_required
def update_livestock(request, pk):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Permission denied!')
        return redirect('livestock-list')
    
    animal = get_object_or_404(Livestock, pk=pk)
    
    if request.method == 'POST':
        animal.animal_type_id = request.POST.get('animal_type')
        animal.breed = request.POST.get('breed')
        animal.tag_number = request.POST.get('tag_number')
        animal.date_of_birth = request.POST.get('date_of_birth')
        animal.gender = request.POST.get('gender')
        animal.status = request.POST.get('status')
        animal.weight = request.POST.get('weight') or None
        animal.notes = request.POST.get('notes', '')
        
        if request.FILES.get('image'):
            animal.image = request.FILES.get('image')
        
        animal.save()
        messages.success(request, f'Livestock {animal.tag_number} updated!')
        return redirect('livestock-detail', pk=animal.pk)
    
    animal_types = AnimalType.objects.all()
    return render(request, 'livestock/update_livestock.html', {
        'animal': animal,
        'animal_types': animal_types
    })

@login_required
def delete_livestock(request, pk):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Permission denied!')
        return redirect('livestock-list')
    
    animal = get_object_or_404(Livestock, pk=pk)
    
    if request.method == 'POST':
        animal.delete()
        messages.success(request, 'Livestock deleted successfully!')
        return redirect('livestock-list')
    
    return render(request, 'livestock/delete_livestock.html', {'animal': animal})

def livestock_stats(request):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Permission denied!')
        return redirect('livestock-list')
    
    # Statistics for dashboard
    total = Livestock.objects.count()
    healthy = Livestock.objects.filter(status='HEALTHY').count()
    sick = Livestock.objects.filter(status='SICK').count()
    sold = Livestock.objects.filter(status='SOLD').count()
    
    # Group by animal type
    by_type = {}
    for animal_type in AnimalType.objects.all():
        count = Livestock.objects.filter(animal_type=animal_type).count()
        if count > 0:
            by_type[animal_type.name] = count
    
    return render(request, 'livestock/livestock_stats.html', {
        'total': total,
        'healthy': healthy,
        'sick': sick,
        'sold': sold,
        'by_type': by_type,
    })