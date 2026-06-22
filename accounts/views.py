from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView,View)
from pyexpat.errors import messages
from unicodedata import category
from django.http import HttpResponse
from .tasks import new_post_message

from .models import Post, Category, PostCategory
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

class PostsList(ListView):
    model = Post
    ordering = 'time_of_posting'
    template_name = 'Posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('accounts.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('accounts.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.publication = 'NW'
        post.save()
        new_post_message.delay(post.pk)
        return super().form_valid(form)

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('accounts.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.publication = 'AT'
        post.save()
        new_post_message.delay(post.pk)
        return super().form_valid(form)

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('accounts.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')

class CategoryListView(PostsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category,id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_of_posting')
        self.filterset = Post.objects.filter(category=self.category).order_by('-time_of_posting')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category']= self.category
        return context

@login_required
def subscribe(request,pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request,'subcribe.html',{'category': category,'message':message})

class IndevView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')