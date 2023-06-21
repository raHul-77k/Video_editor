from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Video
from .models import Effect

# Define the choices for the effect field
EFFECT_CHOICES = (
    ('none', 'No effect'),
    ('grayscale', 'Grayscale'),
    ('sepia', 'Sepia'),
)

class VideoForm(forms.ModelForm):
    image = forms.ImageField()
    effect = forms.ChoiceField(choices=EFFECT_CHOICES)

    class Meta:
        model = Video
        fields = ['title', 'image', 'effect']
