from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.offers.models import Offer


class OfferForm(forms.ModelForm):
    """Form for creation Offer model."""

    class Meta:
        model = Offer
        fields = ('fee',)
        help_texts = {
            'fee': _('Enter fee'),
        }
