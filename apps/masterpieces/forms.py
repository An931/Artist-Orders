from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Masterpiece


class MasterpieceForm(forms.ModelForm):
    """Form for creation Masterpiece model."""

    class Meta:
        model = Masterpiece
        fields = ['title',
                  'description',
                  'tags',
                  # 'files',
                  'visible',
                  ]
        help_texts = {
            'visible': _('Show this for all user'),
        }
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            # 'files': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False)
