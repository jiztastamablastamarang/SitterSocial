from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Vote
from .forms import PostForm
from rest_framework import permissions


class Feed(View):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-date')
        form = PostForm()
        votes = Vote.objects.all()
        print(kwargs)
        context = {
            'form': form,
            'feed': posts,
            'votes': votes,
        }
        return render(request, 'network/feed.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-date')
        votes = Vote.objects.all()
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        context = {
            'form': form,
            'feed': posts,
            'votes': votes,
        }
        return render(request, 'network/feed.html', context)


def VoteView(request, pk):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    vote = int(request.POST.get('vote'))
    kwargs = dict(
        post=post,
        vote=vote,
        user=user,
    )
    unlike = Vote.objects.filter(**kwargs)

    if unlike.exists():
        unlike.delete()
    else:
        Vote.objects.create(**kwargs)

    return redirect('network:feed')


