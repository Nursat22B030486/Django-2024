from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView
from django.db.models import Q 

# Create your views here.
@csrf_exempt 
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    return render(request, 'post/list.html', {'page': page,
                                              'posts': objects})

@csrf_exempt
def post_detail(request, id):
    try: 
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise HttpResponseNotFound('No post found')
    return render(request, 'post/detail.html', {
                                                'post': post,
                                                'user': request.user})


# class CreatePostView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = CreatePostForm
#     template_name = 'post/form.html'
#     success_url = reverse_lazy('post_list')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
    else:
        form = PostForm()
    return render(request, "post/form.html", {"form": form})


# TODO: edit and delete buttom for the author not for all
@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    form = PostForm(request.POST, instance=post)
    if request.method == "POST":    
        if form.is_valid():
            form.save()
            return redirect(f'/posts/{post.id}')
    else:
        form = PostForm(instance=post)
    return render(request, 'post/edit_post.html', {'form': form,})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id, author = request.user)
    if post is  None:
        response = "<h2>You cnan't delete other's post </h2>"
        return HttpResponse(response)
    post.delete()
    return redirect('/')

class AddCommentOnPostView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post/add_comment.html'

    def get_success_url(self):
        # Assuming the comment is linked to a post via a ForeignKey
        post_id = self.object.post.id  # Get the associated post ID from the comment
        return reverse_lazy('post_detail', kwargs={'id': post_id})
    
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['id']
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


# class SearchResultsView(ListView):
#     model = Post
#     template_name = 'post/search.html'

#     def get_queryset(self): # new
#         query = self.request.GET.get("q")
#         result =  Post.objects.filter(
#             Q(title__icontains=query) | Q(author__name__icontains=query) | Q(content__icontains=query)
#         )()
#         if result is None:
#             return HttpResponse("No such results...")
#         return result


