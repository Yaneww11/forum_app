from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, FormView, DeleteView

from forumApp.posts.decorators import measure_execution_time
from forumApp.posts.forms import PostCreateForm, PostDeleteForm, SearchForm, PostEditForm, CommentFormSet
from forumApp.posts.mixins import TimeRestrictedMixin
from forumApp.posts.models import Post


@method_decorator(measure_execution_time, name='dispatch')
@method_decorator(measure_execution_time, name='get')
class Index(TimeRestrictedMixin, View):
    def get(self, request, *args, **kwargs):
        form = modelform_factory(Post, fields=('title', 'content', 'author', 'languages'))
        context = {
            "my_form": form,
        }
        return render(request, 'common/index.html', context)


def dashboard(request):
    form = SearchForm(request.GET)
    posts = Post.objects.all()

    if request.method == "GET":
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = posts.filter(title__icontains=query)

    context = {
        "posts": posts,
        "form": form,
    }

    return render(request, 'posts/dashboard.html', context)


class DashboardView(ListView, FormView):
    model = Post
    template_name = 'posts/dashboard.html'
    context_object_name = 'posts'
    form_class = SearchForm
    paginate_by = 2
    success_url =  reverse_lazy('dash')

    def get_queryset(self):
        queryset = self.model.objects.all()

        if not self.request.user.has_perm('posts.can_approve_posts'):
            queryset = queryset.filter(approved=True)
        else:
            queryset = queryset.order_by('approved', 'created_at')

        if 'query' in self.request.GET:
            query = self.request.GET['query']
            queryset = self.queryset.filter(title__icontains=query)

        return queryset


def approve_post(request, pk: int):
    post = Post.objects.get(pk=pk)
    post.approved = True
    post.save()

    return redirect(request.META.get('HTTP_REFERER'))

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add-post.html'
    success_url = reverse_lazy('dash')


def add_post(request):
    form = PostCreateForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('dash')

    context = {
        "form": form,
    }

    return render(request, 'posts/add-post.html', context)


def edit_post(request, pk: int):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('dash')
    else:
        form = PostEditForm(instance=post)

    context = {
        "form": form,
        "post": post,
    }

    return render(request, 'posts/edit-post.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/details-post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = context['post'].comments.all() # self.object.comments.all()
        context['formset'] = CommentFormSet()
        return context


    def post(self, request, *args, **kwargs):
        post = self.get_object()
        formset = CommentFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    comment = form.save(commit=False)
                    comment.post = post
                    form.save()

            return redirect('details-post', pk=post.id)

        context = self.get_context_data()
        context['formset'] = formset

        return self.render_to_response(context)



def details_page(request, pk: int):
    post = Post.objects.get(pk=pk)
    formset = CommentFormSet(request.POST or None)
    comments = post.comments.all()

    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    comment = form.save(commit=False)
                    comment.post = post
                    form.save()

            return redirect('details-post', pk=post.id)

    context = {
        "post": post,
        "formset": formset,
        "comments": comments,
    }

    return render(request, 'posts/details-post.html', context)

class DeletePageView(DeleteView, FormView):
    model = Post
    template_name = 'posts/delete-post.html'
    success_url = reverse_lazy('dash')
    form_class = PostDeleteForm

    def get_initial(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        post = Post.objects.get(pk=pk)
        return post.__dict__


def delete_post(request, pk: int):
    post = Post.objects.get(pk=pk)
    form = PostDeleteForm(instance=post)

    if request.method == "POST":
        post.delete()
        return redirect('dash')

    context = {
        "form": form,
        "post": post,
    }

    return render(request, 'posts/delete-post.html', context)



