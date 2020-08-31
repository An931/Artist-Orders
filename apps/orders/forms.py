from django import forms
from django.forms import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from apps.orders.models import Order


class OrderForm(forms.ModelForm):
    """Form for creation OrderInfo model."""

    class Meta:
        model = Order
        fields = ['title',
                  'description',
                  'complete_to',
                  'tags',
                  'files',
                  ]
        help_texts = {
            'complete_to': _('Date when order is to be done'),
            'tags': _(
                'Add tags, it help you to find the most suitable artist'
            ),
            'files': _('If you want add some expected examples'),
        }
        widgets = {
            'complete_to': SelectDateWidget(empty_label="Nothing"),
            'tags': forms.CheckboxSelectMultiple(),
        }
