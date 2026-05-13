"""
Формы (forms.py) — описание HTML-форм и их валидации.

ModelForm — форма, автоматически создаваемая на основе модели.
Django сам генерирует поля формы из полей модели и проводит валидацию.

forms.Form — обычная форма без привязки к модели.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Форма бронирования на основе модели Booking.
    
    Meta.fields — список полей, которые будут в форме (остальные заполняются в view).
    widgets — настройка виджетов (HTML-элементов): DateTimeInput → <input type="datetime-local">.
    """

    class Meta:
        model = Booking
        # Перечисляем только те поля, которые заполняет пользователь
        fields = [
            'event_name', 'start_datetime', 'end_datetime',
            'participants_count', 'equipment_needed', 'special_requirements'
        ]
        widgets = {
            # DateTimeInput с type="datetime-local" — нативный пикер даты/времени в браузере
            'start_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'end_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'participants_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'equipment_needed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'event_name': 'Название мероприятия',
            'start_datetime': 'Дата и время начала',
            'end_datetime': 'Дата и время окончания',
            'participants_count': 'Количество участников',
            'equipment_needed': 'Необходимое оборудование',
            'special_requirements': 'Особые требования',
        }


class LoginForm(forms.Form):
    """Форма входа — простая форма без привязки к модели."""
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class RegisterForm(UserCreationForm):
    """
    Форма регистрации — расширяет встроенную UserCreationForm.
    UserCreationForm уже включает поля username, password1, password2 с валидацией.
    Мы добавляем email.
    """
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем Bootstrap-класс к унаследованным полям
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        """Переопределяем save(), чтобы сохранить email."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
