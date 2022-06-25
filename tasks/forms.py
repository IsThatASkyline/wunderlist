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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control no-border'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control no-border'}))


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        # fields = '__all__'
        fields = ['title', 'category', 'user']
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
    content = forms.CharField(widget=forms.Textarea(attrs={'maxlength':'300' ,'cols': 25}), label = '')
    class Meta:
        model = Tasks
        fields = ['content']
        # widgets = {
        #     'content': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'resize': None}, label = ''),
        # }

