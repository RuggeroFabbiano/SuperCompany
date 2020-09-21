from django.views.generic import (ListView, DetailView, UpdateView,  DeleteView,
    CreateView)
from django.db.models import Q
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment
from blog.forms import CommentForm, SignUpForm, PostForm

class PostList(ListView):
    model = Post
    def get_queryset(self):
        relevantPosts = Post.objects.filter(posted=True).order_by('-date')
        if 'search' in self.request.GET:
            searched = self.request.GET['search']
            return relevantPosts.filter(Q(title__icontains=searched) |
                Q(content__icontains=searched) |
                Q(authorInfo__icontains=searched))
        return relevantPosts

class PostDetail(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    def post(self, *args, **kwargs): # to post comments
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
    def get_success_url(self): # auto-redirect when commenting
        return reverse_lazy('blog:article', kwargs={'pk': self.kwargs['pk']})

def subscription(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            UN = form.cleaned_data.get('username')
            PW = form.cleaned_data.get('password1')
            login(request, authenticate(username=UN, password=PW))
            return redirect('blog:journal')
    else:
        form = SignUpForm()
    return render(request, 'registration/subscribe.html', {'form': form})

class EditPost(LoginRequiredMixin, UpdateView):
    login_url = 'blog:login'
    model = Post
    form_class = PostForm
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.title = self.object.title[3:-4]
        self.object.content = self.object.content[3:-4]
        self.object.save()
        return redirect(self.get_success_url())

class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    # success_url = reverse_lazy('blog:journal')
    def get_success_url(self):
        if self.object.posted:
            return reverse_lazy('blog:journal')
        else:
            return reverse_lazy('blog:drafts')

@login_required
def removeComment(request, pk):
    if request.method=='POST':
        comment = Comment.objects.get(pk=pk)
        postID = comment.post.pk
        comment.delete()
    return redirect('blog:article', pk=postID)

class NewPost(LoginRequiredMixin, CreateView):
    login_url = 'blog:login'
    model = Post
    form_class = PostForm
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.authorInfo = self.request.user.get_full_name()
        self.object.title = self.object.title[3:-4]
        self.object.content = self.object.content[3:-4]
        self.object.save()
        return redirect(self.get_success_url())

class DraftList(LoginRequiredMixin, ListView):
    login_url = "blog:login"
    model = Post
    template_name = 'blog/draft_list.html'
    def get_queryset(self):
        relevantPosts = Post.objects.filter(author=self.request.user).filter(posted=False).order_by('-date')
        if 'search' in self.request.GET:
            searched = self.request.GET['search']
            return relevantPosts.filter(Q(title__icontains=searched) |
                Q(content__icontains=searched))
        return relevantPosts
    def get_success_url():
        return reverse_lazy('blog:drafts')
