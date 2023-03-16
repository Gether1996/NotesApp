from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timezone
from viewer.forms import CategoryForm, NoteForm
from viewer.models import *


def base_context():
    all_categories = Category.objects.all()
    return {'all_categories': all_categories}


def homepage(request):
    user_id = request.user.id
    now_utc = datetime.now(timezone.utc)
    notes_ordered_by_time = Note.objects.filter(user_id=user_id, scheduled_time__gte=now_utc, finished=False).order_by('scheduled_time')
    first_note_by_time = notes_ordered_by_time.first()
    try:
        note_with_priority_4 = Note.objects.get(user_id=user_id, finished=False, priority=4)
    except Note.DoesNotExist:
        note_with_priority_4 = None
    if first_note_by_time is not None:
        remaining_time = (first_note_by_time.scheduled_time - now_utc).total_seconds()
        days = int(remaining_time // (24 * 3600))
        seconds = int(remaining_time % (24 * 3600))
        hours = seconds // 3600
        minutes = (seconds // 60) % 60
        seconds = seconds % 60

        if days > 0:
            remaining_time_formatted = f"{days}d:{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
        else:
            remaining_time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        remaining_time_formatted = ''
    context = {
        "first_note_by_time": first_note_by_time,
        "remaining_time_formatted": remaining_time_formatted,
        "note_with_priority_4": note_with_priority_4
    }
    context.update(base_context())
    return render(request, 'homepage.html', context)


@login_required
def user_notes(request):
    notes = Note.objects.filter(user=request.user).order_by('-priority')
    context = {
        'notes': notes
    }
    context.update(base_context())
    return render(request, 'user_notes.html', context)


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
    context.update(base_context())
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
    context.update(base_context())
    return render(request, 'add_note.html', context)


def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('user_notes')
    else:
        form = NoteForm(instance=note)
    context = {
        'form': form,
        'note_id': note_id
    }
    context.update(base_context())
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


def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    context = {
        'note': note
    }
    context.update(base_context())
    return render(request, 'note_detail.html', context)


def filter_notes(request):
    notes = Note.objects.filter(user=request.user)
    category_name = request.GET.get('category')
    priority = request.GET.get('priority')
    finished = request.GET.get('finished')

    if category_name:
        notes = notes.filter(category__name=category_name)

    if priority:
        notes = notes.filter(priority=priority)

    if finished is not None:
        notes = notes.filter(finished=finished)

    context = {
        'notes': notes
    }
    context.update(base_context())
    return render(request, 'filter_notes.html', context)

