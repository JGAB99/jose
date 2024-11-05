from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Exercise

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ExerciseForm(forms.ModelForm):
    user_answer = forms.FloatField(label='Tu respuesta')

    class Meta:
        model = Exercise
        fields = ['user_answer']