from django import forms
from .models import CampingParticipant

class CampingRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию'
    }))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Например: Россия'
    }))
    
    desired_country = forms.ChoiceField(choices=[
        ('Таиланд', 'Таиланд'),
        ('Грузия', 'Грузия'),
        ('Португалия', 'Португалия'),
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('junior', 'Junior разработчик'),
        ('middle', 'Middle разработчик'),
        ('senior', 'Senior разработчик'),
        ('teacher', 'Преподаватель'),
        ('other', 'Другое'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your@email.com'
    }))
    
    class Meta:
        model = CampingParticipant
        fields = ['first_name', 'last_name', 'country', 'desired_country', 'role', 'email']

class TeacherNotificationForm(forms.Form):
    """Форма для уведомления преподавателей о запуске платформы"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
            'required': 'required'
        })
    )
    
    def __str__(self):
        return self.email