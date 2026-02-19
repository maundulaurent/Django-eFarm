from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Article, ArticleCategory

def article_list(request):
    articles = Article.objects.filter(is_published=True)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        articles = articles.filter(category_id=category_id)
    
    # Search
    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    categories = ArticleCategory.objects.annotate(
        article_count=Count('article')
    )
    
    # Popular articles
    popular_articles = Article.objects.filter(
        is_published=True
    ).order_by('-views')[:5]
    
    return render(request, 'blog/article_list.html', {
        'articles': articles,
        'categories': categories,
        'popular_articles': popular_articles,
        'query': query
    })

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    # Increment view count
    article.views += 1
    article.save()
    
    # Related articles
    related_articles = Article.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(pk=article.pk)[:3]
    
    return render(request, 'blog/article_detail.html', {
        'article': article,
        'related_articles': related_articles
    })

@login_required
def add_article(request):
    if request.user.user_type != 'FARMER':
        messages.error(request, 'Only farmers can write articles!')
        return redirect('article-list')
    
    if request.method == 'POST':
        article = Article.objects.create(
            title=request.POST.get('title'),
            slug=request.POST.get('slug'),
            author=request.user,
            category_id=request.POST.get('category'),
            content=request.POST.get('content'),
            excerpt=request.POST.get('excerpt'),
            is_published=request.POST.get('is_published') == 'on'
        )
        
        if request.FILES.get('featured_image'):
            article.featured_image = request.FILES.get('featured_image')
            article.save()
        
        messages.success(request, f'Article "{article.title}" created!')
        return redirect('article-detail', slug=article.slug)
    
    categories = ArticleCategory.objects.all()
    return render(request, 'blog/add_article.html', {'categories': categories})

@login_required
def update_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.user != article.author and request.user.user_type != 'FARMER':
        messages.error(request, 'You can only edit your own articles!')
        return redirect('article-detail', slug=article.slug)
    
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.slug = request.POST.get('slug')
        article.category_id = request.POST.get('category')
        article.content = request.POST.get('content')
        article.excerpt = request.POST.get('excerpt')
        article.is_published = request.POST.get('is_published') == 'on'
        
        if request.FILES.get('featured_image'):
            article.featured_image = request.FILES.get('featured_image')
        
        article.save()
        messages.success(request, 'Article updated successfully!')
        return redirect('article-detail', slug=article.slug)
    
    categories = ArticleCategory.objects.all()
    return render(request, 'blog/update_article.html', {
        'article': article,
        'categories': categories
    })

@login_required
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.user != article.author and request.user.user_type != 'FARMER':
        messages.error(request, 'You can only delete your own articles!')
        return redirect('article-detail', slug=article.slug)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect('article-list')
    
    return render(request, 'blog/delete_article.html', {'article': article})

def category_list(request):
    categories = ArticleCategory.objects.annotate(
        article_count=Count('article')
    )
    return render(request, 'blog/category_list.html', {'categories': categories})