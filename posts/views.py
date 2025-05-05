from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.db.models import Q

@login_required
def post_list(request):
    posts = Post.objects.filter(
        Q(target_type='GE') | 
        Q(department=request.user.department) |
        Q(course__department=request.user.department) |
        Q(professor=request.user)
    ).distinct().order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    return render(request, 'posts/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_list')
    else:
        form = PostForm(user=request.user)
    return render(request, 'posts/post_form.html', {'form': form})