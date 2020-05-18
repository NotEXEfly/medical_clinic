from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from authentication.models import Profile


class RegUserForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'login'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'ivan@mail.ru'})
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': '**********'})
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': '**********'})
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def save(self, commit=True):
        user = super(RegUserForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()

        return user


class RegProfileForm(forms.ModelForm):
    fio = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'})
    )

    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={'placeholder': 'Аватар', 'accept': 'image/jpeg,image/png'})
    )

    class Meta:
        model = Profile
        fields = (
            'fio',
            'avatar'
        )

    def save(self, commit=True):
        profile = super(RegProfileForm, self).save(commit=False)

        profile.fio = self.cleaned_data['fio']
        profile.avatar = self.cleaned_data['avatar']

        if commit:
            profile.save()

        return profile

    def clean_fio(self):
        data = self.cleaned_data
        return data['fio'].lower().title()

    def clean_avatar(self):
        data = self.cleaned_data
        if not data['avatar']:
            return "default.png"
        else:
            return data['avatar']
