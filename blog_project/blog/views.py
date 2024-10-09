from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

# Create your views here.
@csrf_exempt 
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, 'post/list.html', {'posts': posts})

@csrf_exempt
def post_detail(request, id):
    try: 
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise HttpResponseNotFound('No post found')
    return render(request, 'post/detail.html', {'post': post})


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
    return render(request, 'post/edit_post.html', {'form': form})

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




