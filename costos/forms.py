from django import forms
from .models import  Restaurant, Provider, Ingredient, Receta, Steps
from django.forms import ModelForm, HiddenInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Hidden


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'account_id',
            'phone',

        ]


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = [
            'name',
            'description',
            'extra_street',
            'street',
            'city',
            'state',
            'zip_code',
            'contact',
            'email',
            'web',
        ]


class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = [
            'name',
            'description',
            'extra_street',
            'street',
            'city',
            'state',
            'chefs'
        ]


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = [

            'provider',
            'name',
            'description',
            'presentation',
            'type',
            'price',
            'qty',
            'error',

        ]


class RecetaForm(forms.ModelForm):

    class Meta:
        model = Receta
        fields = [

            'restaurant',
            'name',
            'description',
            'portions',
            'items',
        ]


class StepsForm(forms.ModelForm):

    class Meta:
        model = Steps
        fields = [
            'qty',
            'error',
            'preparation',
            'duration',
        ]


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username','email','password1','password2','first_name','last_name')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

