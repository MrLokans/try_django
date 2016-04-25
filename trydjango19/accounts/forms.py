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


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)

        if email_qs.count() > 0:
            msg = "Username with email {} already exists."
            raise forms.ValidationError(msg.format(email))
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password
