from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.http import Http404
# Create your views here.


def post_list(request):
    post_list_one_page = Post.published.all()
    paginator = Paginator(post_list_one_page, 2)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


class PostListView(ListView):
    queryset = Post.published.all()
    template_name = 'blog/post/list.html'
    paginate_by = 2
    context_object_name = 'posts'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post,
                              id=post_id,
                              status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()

    return render(request,
                  'blog/post/share',
                  {'posts': post, 'form': form})
