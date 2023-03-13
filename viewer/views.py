from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timezone, timedelta
from viewer.forms import CategoryForm, NoteForm
from viewer.models import *


def homepage(request):
    user_id = request.user.id
    now_utc = datetime.now(timezone.utc)
    notes_ordered = Note.objects.filter(user_id=user_id, scheduled_time__gte=now_utc).order_by('scheduled_time')
    first_note = notes_ordered.first()
    if first_note is not None:
        remaining_time = (first_note.scheduled_time - now_utc).total_seconds()
        days = int(remaining_time // (24 * 3600))
        seconds = int(remaining_time % (24 * 3600))
        hours = seconds // 3600
        minutes = (seconds // 60) % 60
        seconds = seconds % 60

        if days > 0:
            remaining_time_formatted = f"{days}d:{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
        else:
            remaining_time_formatted = f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
    else:
        remaining_time_formatted = ''
    return render(request, 'homepage.html', {"first_note": first_note, "remaining_time_formatted": remaining_time_formatted})


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



