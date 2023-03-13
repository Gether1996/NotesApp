from django import forms
from viewer.models import Category, Note


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = "__all__"
        exclude = ["user"]

