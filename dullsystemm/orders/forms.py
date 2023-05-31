from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name= forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={'class': 'form-input'}))
    postal_code = forms.CharField(label='Почтовый', widget=forms.TextInput(attrs={'class': 'form-input'}))
    city = forms.CharField(label='Город', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
