from django.shortcuts import render, redirect
from django.contrib.auth import logout
from accounts.forms import CustomUserCreationForm


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'registration.html', context)


def logout_view(request):
    logout(request)
    return redirect('homepage')


def profile(request):
    return render(request, "profile.html")
