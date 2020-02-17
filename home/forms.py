from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, PasswordInput

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)
        widgets = {
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'First Name', 'help_text': 'Optional'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'Last Name', 'help_text': 'Optional'}),
            #'business_name': TextInput(attrs={'class': 'input', 'placeholder': 'Business Name', 'help_text': 'Optional'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'E-mail', 'help_text': 'Required. Inform a vaild e-mail address'}),
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'Username'}),
            'password1': PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'}),
            'password2': PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm Password'}),

        }

        def clean_username(self):
            username = self.cleaned_data.get('username')
            qs = User.objects.filter(username=username)
            if qs.exists():
                raise forms.ValidationError("Username is taken")
            return username

        def clean_email(self):
            email = self.cleaned_data.get('email')
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("E-mail address is taken")
            return email

        def clean(self):
            data = self.cleaned_data
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password2 != password1:
                raise forms.ValidationError("Passwords must match.")
            return data

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    first_name = forms.CharField(widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password ', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("E-mail address is taken")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("Passwords must match.")
        return data
