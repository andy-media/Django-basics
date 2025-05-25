from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Blog, Comment
from django.db.models import Q
from django.http import HttpResponse
import os
# Create your views here.

def debug_cloudinary(request):
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    # Test Cloudinary configuration
    try:
        # Get Cloudinary configuration
        cloud_name = cloudinary.config().cloud_name
        api_key = cloudinary.config().api_key
        api_secret = cloudinary.config().api_secret
        
        # Test Cloudinary API
        result = cloudinary.api.ping()
        
        # Get a list of all resources
        resources = cloudinary.api.resources()
        
        # Format the response
        response = f"<h2>Cloudinary Configuration</h2>"
        response += f"<p>CLOUD_NAME: {cloud_name}</p>"
        response += f"<p>CLOUD_API_KEY: {api_key}</p>"
        response += f"<p>CLOUD_API_SECRET: {api_secret}</p>"
        
        response += f"<h2>Cloudinary API Test</h2>"
        response += f"<p>Ping Result: {result}</p>"
        
        response += f"<h2>Cloudinary Resources</h2>"
        response += "<ul>"
        for resource in resources.get('resources', []):
            response += f"<li><img src='{resource['url']}' width='100'> {resource['public_id']} - {resource['url']}</li>"
        response += "</ul>"
        
        return HttpResponse(response)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


# Create your views here.
def index(request):
    section = request.GET.get('section', 'Popular')  # Default to 'Popular' if none
    page = request.GET.get('page', 1)  # Get the page parameter, default to 1

    # Filter based on selected section
    filtered_posts = Blog.objects.filter(section=section).order_by('-id')[:5]

    # Get all posts for pagination
    all_posts = Blog.objects.order_by('-id')
    
    # Paginate the posts - 4 posts per page
    paginator = Paginator(all_posts, 4)
    
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_posts = paginator.page(paginator.num_pages)
    
    # Get other required data
    main_post = Blog.objects.filter(main_post=True).order_by('id')
    recent = Blog.objects.filter(section='Recent').order_by('-id')[:1]
    popular = Blog.objects.filter(section='Popular').order_by('-id')[:4]
    trending_posts = Blog.objects.filter(section='Trending').order_by('-id')
    highlights = Blog.objects.filter(category__name='Highlights').order_by('-id')
    news = Blog.objects.filter(category__name='News').order_by('-id')
    main_trend_1 = trending_posts[:1]
    main_trend_2 = trending_posts[1:2]
    more_trending_1 = trending_posts[2:4]
    more_trending_2 = trending_posts[4:6]
    cat = Category.objects.all()
    
    context = {  
        'post': all_posts,
        'posts': paginated_posts,
        'filtered_posts': filtered_posts,
        'main_post': main_post,
        'recent': recent, 
        'cat': cat,
        'popular': popular,
        'main_trend_1': main_trend_1,
        'main_trend_2': main_trend_2,
        'more_trending': more_trending_1,
        'more_trending2': more_trending_2,
        'highlights': highlights,
        'news': news,
    }

    return render(request, 'website/index.html', context)
 
def blog_detail(request, slug):
    category = Category.objects.all()
    popular = Blog.objects.filter(section='Popular').order_by('-id')[:3]
    post = get_object_or_404(Blog, blog_slug = slug)
    comments = Comment.objects.filter(blog_id = post.id).order_by('-date')
    context = { 
        'category': category,
        'cat': category,
        'post': post,
        'comments': comments,
        'popular': popular,
    }
    return render(request, 'website/blog-single.html', context)


def category(request, slug):
    page = request.GET.get('page', 1)  # Get the page parameter, default to 1
    
    cat = Category.objects.all()
    blog_cat = Category.objects.filter(slug=slug)
    popular = Blog.objects.filter(section='Popular').order_by('-id')[:3]
    
    # Get all blogs for the category
    category_obj = get_object_or_404(Category, slug=slug)
    all_category_blogs = category_obj.category.all().order_by('-id')
    
    # Paginate the category blogs - 6 posts per page
    paginator = Paginator(all_category_blogs, 6)
    
    try:
        paginated_blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_blogs = paginator.page(paginator.num_pages)
    
    context = {
        'cat': cat,
        'blog_cat': blog_cat,
        'active_category': slug,
        'popular': popular,
        'paginated_blogs': paginated_blogs,
        'category_obj': category_obj,
    }
    return render(request, 'website/category.html', context)

def about(request):
    cat = Category.objects.all()
    popular = Blog.objects.filter(section='Popular').order_by('-id')[:3]
    context = {
        'cat':cat,
        'popular':popular,
    }
    return render(request, 'website/about.html', context)

def contact(request):
    return render(request, 'website/contact.html')

def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Blog, blog_slug = slug)
        comment_text = request.POST.get('InputComment')
        email = request.POST.get('InputEmail')
        website = request.POST.get('InputWeb')
        name = request.POST.get('InputName')
        parent_id = request.POST.get('parent_id')
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        Comment.objects.create(
            post = post,
            name = name,
            email = email,
            website = website,
            comment = comment_text,
            parent=parent_comment,
        )
        return redirect('blog_detail', slug=post.blog_slug)
    return redirect('blog_detail')


def search_view(request):
    category = Category.objects.all()
    query = request.GET.get('q', '').strip()

    results = Blog.objects.filter(
    Q(title__icontains=query) | Q(content__icontains=query),
    status='1'
) if query else []
    print("QUERY:", query)
    print("RESULTS COUNT:", len(results))
    context = {
        'query': query,
        'results': results,
        'cat': category,
    }
    return render(request, 'website/search_results.html', context)
