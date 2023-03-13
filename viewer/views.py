from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from viewer.forms import CategoryForm, NoteForm
from viewer.models import *


def homepage(request):
    return render(request, 'homepage.html')


@login_required
def user_notes(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'user_notes.html', {'notes': notes})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'add_category.html', context)


@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('user_notes')
    else:
        form = NoteForm()
    context = {
        'form': form
    }
    return render(request, 'add_note.html', context)


def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = NoteForm(instance=note)
    context = {
        'form': form,
        'note_id': note_id
    }
    return render(request, 'edit_note.html', context)


def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('user_notes')


def finish_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        note.finished = True
        note.save()
        return redirect('user_notes')



