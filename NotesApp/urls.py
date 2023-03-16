"""NotesApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts.views import logout_view, registration
from viewer.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name="homepage"),
    path('accounts/logout/', logout_view),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/', registration, name='registration'),
    path('accounts/profile/', homepage, name='profile'),
    path('user_notes/', user_notes, name='user_notes'),
    path('add_note/', add_note, name='add_note'),
    path('add_category/', add_category, name='add_category'),
    path('notes/<int:note_id>/edit/', edit_note, name='edit_note'),
    path('notes/<int:note_id>/delete/', delete_note, name='delete_note'),
    path('notes/<int:note_id>/finish/', finish_note, name='finish_note'),
    path('note_detail/<int:note_id>/', note_detail, name='note_detail'),
    path('filter/', filter_notes, name='filter_notes'),
]
