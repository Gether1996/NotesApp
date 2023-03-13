from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage.html')


def user_notes(request):
    return render(request, 'user_notes.html')
