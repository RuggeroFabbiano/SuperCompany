"""
Views module for blog app.
"""

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import FormMixin
from .models import Post, Comment
from .forms import CommentForm, SignUpForm, PostForm

class PostList(ListView):
    """
    View for listing posted articles
    """

    model = Post
    def get_queryset(self):
        relevant_posts = Post.objects.filter(posted=True).order_by('-date')
        if 'search' in self.request.GET:
            searched = self.request.GET['search']
            return relevant_posts.filter(Q(title__icontains=searched) |
                Q(content__icontains=searched) |
                Q(authorInfo__icontains=searched))
        return relevant_posts

class PostDetail(FormMixin, DetailView):
    """
    View to show details of selected post
    """

    model = Post
    form_class = CommentForm
    def post(self, *args, **kwargs): # to post comments
        """
        Re-definition of post method for article post objects
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = get_object_or_404(Post, pk=self.object.pk)
            comment.author = self.request.user
            comment.authorInfo = self.request.user.get_full_name()
            comment.content = comment.content[3:-4]
            form.save()
            return super().form_valid(form)
        return None
    def get_success_url(self):
        """
        Auto-redirect when commenting
        """
        return reverse_lazy('blog:article', kwargs={'pk': self.kwargs['pk']})

def subscription(request):
    """
    Handle signing up form and behaviour
    """
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            pass_word = form.cleaned_data.get('password1')
            login(request, authenticate(username=user_name, password=pass_word))
            return redirect('blog:journal')
    else:
        form = SignUpForm()
    return render(request, 'registration/subscribe.html', {'form': form})

class EditPost(LoginRequiredMixin, UpdateView):
    """
    View that allows to edit an already published blog post
    """

    login_url = 'blog:login'
    model = Post
    form_class = PostForm
    def form_valid(self, form):
        """
        Handle behaviour if edited post is valid
        """
        self.object = form.save(commit=False)
        self.object.title = self.object.title[3:-4]
        self.object.content = self.object.content[3:-4]
        self.object.save()
        return redirect(self.get_success_url())

class DeletePost(LoginRequiredMixin, DeleteView):
    """
    View to delete post objects
    """

    model = Post
    def get_success_url(self):
        """
        Re-define destination URL after successful deletion
        """
        if self.object.posted:
            return reverse_lazy('blog:journal')
        return reverse_lazy('blog:drafts')

@login_required
def remove_comment(request, pk):
    """
    View to delete comment under post
    """
    if request.method=='POST':
        comment = Comment.objects.get(pk=pk)
        post_id = comment.post.pk
        comment.delete()
    return redirect('blog:article', pk=post_id)

class NewPost(LoginRequiredMixin, CreateView):
    """
    View to write new post article
    """

    login_url = 'blog:login'
    model = Post
    form_class = PostForm
    def form_valid(self, form):
        """
        Handle behaviour if inserted article is valid
        """
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.authorInfo = self.request.user.get_full_name()
        self.object.title = self.object.title[3:-4]
        self.object.content = self.object.content[3:-4]
        self.object.save()
        return redirect(self.get_success_url())

class DraftList(LoginRequiredMixin, ListView):
    """
    Shows list of unpublished post of the logged-in user
    """

    login_url = "blog:login"
    model = Post
    template_name = 'blog/draft_list.html'
    def get_queryset(self):
        """
        Get objects filtering by logged user
        """
        relevant_posts = Post.objects.filter(author=self.request.user)
        relevant_posts = relevant_posts.filter(posted=False).order_by('-date')
        if 'search' in self.request.GET:
            searched = self.request.GET['search']
            return relevant_posts.filter(Q(title__icontains=searched) |
                Q(content__icontains=searched))
        return relevant_posts
    def get_success_url():
        """
        Re-define destination URL if successful
        """
        return reverse_lazy('blog:drafts')
