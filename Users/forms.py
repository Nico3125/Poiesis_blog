from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Poems


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']


class PoemForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'special'}))
    body = forms.CharField(required=True, widget=forms.Textarea(
        attrs={"placeholder": "Your poem here", "class": "textarea is-success is-medium"}))

    class Meta:
        model = Poems

        exclude = ("user",)

class EditPoemForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField()

    class Meta:
        model = Poems

        exclude = ("user",)