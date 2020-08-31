from django import forms

from apps.users.models import User


class UserForm(forms.ModelForm):
    """Form for creation User model."""

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'phone_number',
        ]

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        """Check if passed data valid."""
        super().clean()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            msg = 'Passwords are not equal'
            self.add_error('confirm_password', msg)
