from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import PoemForm, CreateUserForm
from .models import Profile, Poems


#
# @login_required
def dashboard(request):
    form = PoemForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            poem = form.save(commit=False)
            poem.user = request.user
            poem.save()
            return redirect("Users:dashboard")
    # followed_poems = Poems.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by("-created_at")
    # {"poems": followed_poems}
    return render(request, "Users/dashboard.html", {"form": form, 'poems': Poems.objects.all()})


def add_poems(request):
    form = PoemForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            poem = form.save(commit=False)
            poem.user = request.user
            messages.success(request, f'Congrats! You just posted your poem!')
            poem.save()
            return redirect("Users:my_account")
    context = {
        "form": form,
        'poems': Poems.objects.all()}
    return render(request, 'Users/add_poems.html', context)


#
# def edit_poems(request, pk):
#      # poems = get_object_or_404(Poems, pk=pk)
#     poem_id= get_object_or_404(Poems, pk=pk)
#     # If this is a POST request then process the Form data
#     if request.method == "POST":
#         if request.POST['title'] or request.POST['body']:
#             poem = Poems(pk=pk)
#             poem.title = request.POST['title']
#             poem.body = request.POST['body']
#             poem.save(pk=pk)
#             return render(request, 'Users/my_account.html', {'poem': poem})
#
#         else:
#             return render(request, 'Users/edit_poems.html', {'error': 'Could not edit this poem!'})
#     form = EditPoemForm(request.POST or None)
#     context = {
#         "form": form,
#         'poem_id': poem_id}
#
#     return render(request, 'Users/edit_poems.html', context) (page loading)


# def edit_poems(request, pk):
#     edited = EditPoemForm(request.POST or None)
#     context = {
#         "edited": edited,
#         'poems': Poems.objects.all()}
#     if request.method == "POST":
#         if request.POST['title'] or request.POST['body']:
#             poem = Poems(pk=pk)
#             poem.title = request.POST['title']
#             poem.body = request.POST['body']
#             poem.save(pk=pk)
#             return render(request, 'Users/my_account.html', {'poem': poem})
#
#         else:
#             return render(request, 'Users/edit_poems.html', {'error': 'Could not edit this poem!'})
#     else:
#         return render(request, 'Users/edit_poems.html', context)


from django.views.generic.edit import UpdateView, DeleteView




# @login_required:

# class EditPoems(UpdateView):
#     model = Poems
#     template_name = 'Users/edit_poems.html'
#     fields=[ 'title', 'body',]
#
#     def edit_poems(request):
#         form = PoemForm(request.POST or None)
#         if request.method == "POST":
#             if form.is_valid():
#                 poem = form.save(commit=False)
#                 poem.user = request.user
#                 messages.success(request, f'Congrats! You just posted your poem!')
#                 poem.save()
#                 return redirect("Users:my_account")
#         context = {
#             "form": form,
#             'poems': Poems.objects.all()}
#         return render(request, 'Users/add_poems.html', context)


def read_poems(request):
    poems= Poems.objects.all()
    return render(request, 'Users/read_poems.html',{"poems": poems})




def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user.id)

    return render(request, "Users/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()
    user_profile = Profile.objects.get(pk=pk)

    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(user_profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(user_profile)
        current_user_profile.save()
    return render(request, "Users/profile.html", {"profile": user_profile})


#
def profile_view(request):
    p = request.user.profile
    you = p.user
    # users = Profile.objects.all()
    follows = p.follows.all()
    context = {
        # 'users': users,
        'followers': follows.count
    }
    return render(request, "Users/my_account.html", context)


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Congratulations! You have registered an account for {username}!')
            form.save()
            return redirect('Users:login')
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def login(request):
    context = {}
    return render(request, 'registration/login.html', context)


def logout(request):
    context = {}
    return render(request, 'registration/logout.html', context)
