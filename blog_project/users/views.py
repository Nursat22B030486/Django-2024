from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User 
from .forms import CreateProfileForm, CreateUserForm, ChangeProfileForm, ChangeUserForm
from .models import Profile, Follow

# Create your views here.
def login_user(request):
    # form = LoginForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "there was error in login. Try again! ")
            return redirect('/users/login_user/')
    else:
        return render(request, 'authenticate/login.html', {})
    
def register(request):
    user_form = CreateUserForm()
    profile_form = CreateProfileForm()
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        profile_form = CreateProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user.set_password(user_form.cleaned_data['password1'])  # Hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, ("Registration Successfull!!!"))
            return redirect('/users/login_user/')
    return render(
        request, 
        'authenticate/register.html',
          {'profile_form': profile_form,
           'user_form': user_form})

@login_required
def profile_detail(request, id):
    return render(request, 'authenticate/profile.html', {'user': request.user})

def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    profile = user.profile 
    is_following = False 
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user, following=user
        ).exists()

    followers_count = user.user_follower.count()  # Users following this user
    following_count = user.user_following.count()  # Users this user is following

    context = {
        'user': request.user,
        'profile': profile,
        'is_following': is_following,
        'followers': followers_count,
        'following': following_count,
    }
    return render(request, 'authenticate/profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = request.user.profile
    # TODO: edit_profile button should not be shown on others profilex
    if request.method == "POST":
        user_form = ChangeUserForm(request.POST, instance=user)
        profile_form = ChangeProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile', user.id)
    else:
        user_form = ChangeUserForm(instance=user)
        profile_form = ChangeProfileForm(instance=profile)
    return render(
        request, 
        'authenticate/edit_profile.html',
          {'profile_form': profile_form,
           'user_form': user_form}) 

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def follow_user(request, id):
    user_to_follow = get_object_or_404(User, id = id)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('users:profile', id=id)

@login_required
def unfollow_user(request, id):
    user_to_unfollow = get_object_or_404(User, id=id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('users:profile', id=id) 