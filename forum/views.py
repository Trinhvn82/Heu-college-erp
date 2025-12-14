from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ForumPost, Like, Reply, ForumPostImage, ReplyImage
from .forms import ForumPostForm, ReplyForm


@login_required
def forum_list(request):
    posts = ForumPost.objects.order_by('-created_at')
    # Like xử lý
    if request.method == 'POST' and 'like_post_id' in request.POST:
        post_id = request.POST.get('like_post_id')
        post = ForumPost.objects.get(id=post_id)
        Like.objects.get_or_create(user=request.user, post=post)
        return redirect('forum_list')
    return render(request, 'forum/forum_list.html', {'posts': posts})



@login_required
def forum_create(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                if i >= 3:
                    break
                ForumPostImage.objects.create(post=post, image=image)
            return redirect('forum_list')
    else:
        form = ForumPostForm()
    return render(request, 'forum/forum_create.html', {'form': form})



@login_required
def forum_detail(request, post_id):
    post = ForumPost.objects.get(id=post_id)
    replies = post.replies.order_by('created_at')
    reply_form = ReplyForm()

    # Xử lý like
    if request.method == 'POST' and 'like_post_id' in request.POST:
        if not post.likes.filter(user=request.user).exists():
            Like.objects.create(user=request.user, post=post)
        return redirect('forum_detail', post_id=post.id)

    # Xử lý reply
    if request.method == 'POST' and 'reply_content' in request.POST:
        reply_form = ReplyForm(request.POST, request.FILES)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.author = request.user
            reply.post = post
            reply.save()
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                if i >= 3:
                    break
                ReplyImage.objects.create(reply=reply, image=image)
            return redirect('forum_detail', post_id=post.id)

    liked = post.likes.filter(user=request.user).exists()
    return render(request, 'forum/forum_detail.html', {
        'post': post,
        'replies': replies,
        'reply_form': reply_form,
        'liked': liked,
        'like_count': post.likes.count(),
    })
