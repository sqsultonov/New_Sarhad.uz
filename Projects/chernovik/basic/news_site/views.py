from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from django.db.models import Q
from django.core.paginator import Paginator

# Asosiy sahifa (Home)
def home(request):
    ctg = Category.objects.all()
    featured_qs = Post.objects.filter(is_featured=True).order_by('-created_at')

    featured_posts = []
    for i in range(0, len(featured_qs), 3):
        featured_posts.append(featured_qs[i:i + 3])

    # 2. Eng ko'p ko'rilgan 5 ta
    trending_posts = Post.objects.all().order_by('-views')[:5]
    # Video bloki uchun ko'p ko'rilgan maqolalar 10 ta
    # Video fayli mavjud bo'lgan postlarnigina olamiz
    video_posts = Post.objects.filter(is_video=True).exclude(video_file='').order_by('-created_at')[:10]
    video_posts = Post.objects.filter(is_video=True).order_by('-created_at')[:10]
    # 3. Oxirgi maqolalar (Slayderga kirmaganlari)
    latest_posts = Post.objects.filter(is_featured=False).order_by('-created_at')[:8]
    # Bosh sahifada "Ko'proq" tugmasi uchun
    all_posts_list = Post.objects.filter(is_featured=False).order_by('-created_at')
    paginator = Paginator(all_posts_list, 9)  # 9 ta maqola (3x3 format)
    page_number = request.GET.get('page')
    latest_posts = paginator.get_page(page_number)

    ctx = {
        'ctg': ctg,
        'featured_posts': featured_posts,
        'trending_posts': trending_posts,
        'video_posts': video_posts,
        'latest_posts': latest_posts,
    }
    return render(request, 'blog/index.html', ctx)

# Maqolani o'qish sahifasi
def singlepost_page(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()

    ctg = Category.objects.all()
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id).order_by('-created_at')[:4]
    recent_posts = Post.objects.exclude(id=post.id).order_by('-created_at')[:4]
    popular_posts = Post.objects.exclude(id=post.id).order_by('-views')[:4]

    ctx = {
        'post': post,
        'ctg': ctg,
        'recent_posts': recent_posts,
        'related_posts': related_posts,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/single-post.html', ctx)

# Kategoriya sahifasi (Pagination qo'shilgan)
def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts_list = Post.objects.filter(category=category).order_by('-created_at')

    # Mashhur maqolalar (ko'rishlar soni bo'yicha)
    popular_posts = Post.objects.filter(category=category).order_by('-views')[:5]

    # 9 ta maqola (3x3 format uchun)
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    ctg = Category.objects.all()

    ctx = {
        'category': category,
        'posts': posts,
        'popular_posts': popular_posts,
        'ctg': ctg,
    }
    return render(request, 'blog/category.html', ctx)

# Qidiruv natijalari funksiyasi
def search_results(request):
    query = request.GET.get('search')
    if query:
        posts_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        posts_list = Post.objects.none()

    # Qidiruvda ham 9 tadan va Load More ishlashi uchun:
    paginator = Paginator(posts_list, 9)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    ctg = Category.objects.all()
    ctx = {
        'posts': posts,
        'query': query,
        'ctg': ctg,
    }
    return render(request, 'blog/category.html', ctx)

# Statik sahifalar
def contact_page(request):
    ctg = Category.objects.all()
    return render(request, 'blog/contact.html', {'ctg': ctg})

def elements_page(request):
    ctg = Category.objects.all()
    return render(request, 'blog/elements.html', {'ctg': ctg})