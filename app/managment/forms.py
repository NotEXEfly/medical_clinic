from django import forms
from django.forms import Textarea
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('subject', 'sender', 'message')

        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': 'Тема сообщения'
            }),
            'sender': forms.TextInput(attrs={
                'placeholder': 'Ваш e-mail',
                'type': 'email'
            }),
            'message': Textarea(attrs={
                'cols': 60,
                'rows': 10,
                'placeholder': 'Ваше сообщение',
                'minlength': 10
            }),
        }
