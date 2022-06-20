from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Profile
from .forms import * #PostCreateForm,UserLoginForm,UserRegistrationForm
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    posts_list = Post.objects.all() .order_by('-id')
    query = request.GET.get('q')
    if query:
        posts_list = Post.objects.filter(
        Q(author__username= query) |
        Q(title__contains= query) |
        Q(body__contains= query)
        )
    paginator = Paginator(posts_list,4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'post_list.html',{'posts':posts})

def post_detail(request,id,slug):
    post = get_object_or_404(Post,id=id,slug=slug)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    return render(request,'post_detail.html',{'post':post, 'is_liked':is_liked})

def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post,id = post_id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    post.likes.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())

def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('post_list')
        else:
            return HttpResponse("Invalid Form")
    else:
        form = PostCreateForm()
        return render(request,'post_create.html',{'form':form})

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect('post_list')
                else:
                    return HttpResponse('Username not have permission')
            else:
                return HttpResponse('Username and Password not Valid')
    else:
        form = UserLoginForm()
        return render(request,'login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('user_login')
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html',{'form':form})
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(data = request.POST or None, instance = request.user)
        profile_form = ProfileEditForm(data = request.POST or None, instance = request.user.Profile, files= request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
        return render(request,'edit_profile.html',{'user_form':user_form, 'profile_form':profile_form})
