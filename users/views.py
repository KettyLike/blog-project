from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})