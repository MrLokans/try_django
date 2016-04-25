from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if not (username and password):
            raise forms.ValidationError("Password or username is not present.")

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("This user does not exist.")

        if not user.is_active:
            raise forms.ValidationError("This user is not active.")
        return super().clean(*args, **kwargs)
