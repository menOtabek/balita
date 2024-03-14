from django.shortcuts import render, redirect
from .models import Post, Contact, Comment, Category, Tag
import requests
from django.core.paginator import Paginator

BOT_TOKEN = '6791913442:AAG7cVQzAAwUYj2OQB2jVnpwxl3VGP44Fuc'
CHAT_ID = '5937168278'


def home_view(request):
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    page_obj = Paginator(posts, per_page=3)
    page = request.GET.get('page', 1)
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'home': 'active',
        'rarely_posts': posts.order_by('comment_count')[:6],
        'popular_posts': posts.order_by('-count_view')[:4],
        'latest_posts': posts.order_by('-created_at')[:4],
        'first_posts': posts.order_by('created_at')[:6:-1],
        'posts': page_obj.get_page(page)
    }
    return render(request, 'index.html', context=context)


def blog_detail_view(request, pk):
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(name=data['name'], email=data['email'], message=data['message'], post_id=pk)
        obj.save()
        return redirect(f'/home/{pk}')
    post = Post.objects.get(id=pk)
    post.count_view += 1
    post.save(update_fields=['count_view'])
    post.comment_count += 1
    post.save(update_fields=['comment_count'])

    comments = Comment.objects.filter(post_id=pk, is_view=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_published=True)
    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'comments_count': len(comments),
        'popular_posts': posts.order_by('-count_view')[:4],
        'latest_posts': posts.order_by('-created_at')[:4],
        'categories': categories,
    }

    return render(request, 'blog-single.html', context=context)


def category_view(request):
    categories = Category.objects.all()
    data = request.GET
    page = data.get('page', 1)

    cat = data.get('cat')
    if cat.isnumeric():
        cat_name = Category.objects.filter(id=cat).first()
    else:
        cat_name = Category.objects.filter(name=cat).first()
    posts = Post.objects.filter(is_published=True, category=cat_name)
    popular_posts = Post.objects.filter(is_published=True)
    page_obj = Paginator(posts, per_page=2)
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'posts': page_obj.get_page(page),
        'tags': tags,
        'popular_posts': popular_posts.order_by('-count_view')[:4],
        'latest_posts': popular_posts.order_by('-created_at')[:4],
        "cat_name": cat_name.name
    }
    return render(request, 'category.html', context=context)


def about_view(request):
    data = request.GET
    page = data.get('page', 1)
    posts = Post.objects.filter(is_published=True)
    page_obj = Paginator(posts.order_by('-created_at')[:6], 2)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags': tags,
        'popular_posts': posts.order_by('-count_view')[:4],
        'latest_posts': posts.order_by('-created_at')[:5],
        'about': 'active',
        'posts': page_obj.get_page(page)
    }
    return render(request, 'about.html', context=context)


def contact_view(request):
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(name=data['name'], phone=data['phone'], email=data['email'],
                                     message=data['message'])
        obj.save()
        text = f"""
              project : Balita || Contactdan
              id : {obj.id}
              name : {obj.name}
              message : {obj.message}
              timestamp : {obj.created_at}
              """
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'
        response = requests.get(url)
        print(response)
        return redirect('/contact')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_published=True)
    context = {
        'categories': categories,
        'tags': tags,
        'popular_posts': posts.order_by('-count_view')[:4],
        'latest_posts': posts.order_by('-created_at')[:4],
        'contact': 'active'
    }
    return render(request, 'contact.html', context=context)


def search_view(request):
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')
    query = request.GET.get('q')
    if query is not None and len(query) >= 1:
        posts = Post.objects.filter(is_published=True, title__icontains=query, description__icontains=query)
    else:
        posts = Post.objects.filter(is_published=True)
    d = {'posts': posts,
         'categories': Category.objects.all()}

    return render(request, 'category.html', context=d)


def tag_view(request):
    data = request.GET
    tag_id = data.get('tag')
    categories = Category.objects.all()
    tags = Tag.objects.all()


    if tag_id:
        posts = Post.objects.filter(is_published=True, tag=tag_id)
    else:
        posts = Post.objects.filter(is_published=True)
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'first_posts': posts.order_by('created_at')[:6:-1],
        'popular_posts': posts.order_by('-count_view')[:4],
        'rarely_posts': posts.order_by('comment_count')[:6],
        'latest_posts': posts.order_by('-created_at')[:4],
    }
    return render(request, 'index.html', context=context)
