from django import forms
from .models import Tasks, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control no-border', 'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control no-border', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control no-border', 'placeholder': 'Confirm password'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control no-border', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control no-border', 'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control no-border', 'placeholder': 'Password'}))


class CreateTasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control no-border', 'placeholder': 'Add an item...'})
        }

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control no-border', 'placeholder': 'Add an item...'})
        }

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'create-category', 'placeholder': 'Add category...', 'id': 'create_category'}),

        }

class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class UpdateTaskContentForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'maxlength':'200', 'cols': 20, 'resize': None}),
        }
        labels = {
            'content': '',
        }
