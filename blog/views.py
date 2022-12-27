from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse_lazy

from .forms import NewPostForm
from .models import Post

# def post_list_views(request):
#     post_list = Post.objects.filter(status='pub').order_by('-datetime_modified')
#
#     return render(request, 'blog/posts_list.html', {'post_list': post_list})


class PostListView(generic.ListView):
    template_name = 'blog/posts_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_modified')


# def post_detail_views(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_details.html', {'post': post})
class PostDetailViews(generic.DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'


# def post_add_view(request):
#     if request.method == 'POST':
#         form = NewPostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('post_list')
#
#     else:  # Get Request
#         form = NewPostForm()
#
#     return render(request, 'blog/post_create.html', context={'form': form})

class PostCreateView(generic.CreateView):
    form_class = NewPostForm
    template_name = 'blog/post_create.html'


# def post_update_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     form = NewPostForm(request.POST or None, instance=post)
#     if form.is_valid():
#         form.save()
#         return redirect('post_list')
#
#     return render(request, 'blog/post_create.html', context={'form': form})

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'blog/post_create.html'


# def post_delete_view(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         return redirect('post_list')
#
#     return render(request, 'blog/post_delete.html', context={'post': post})
class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')
