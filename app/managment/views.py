from django.shortcuts import render
from .forms import ContactForm


def contact(request):

    if request.POST:
        form = ContactForm(request.POST)
        # Если форма заполнена корректно, сохраняем все введённые пользователем значения
        if form.is_valid():
            form.save()
        return render(request, 'lk/contact.html', {'form': form, 'valid_status': '1'})
    else:
        form = ContactForm()
        return render(request, 'lk/contact.html', {'form': form})
