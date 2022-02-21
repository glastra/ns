from django import forms
from .models import Company
from .models import Restaurant
from .models import Provider
from .models import Ingredient
from .models import Receta
from .models import Steps
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
            'address',
            'city',
            'state',
            'country',
            'contacto',

        ]

class CompanyForm(forms.ModelForm):


    class Meta:
        model = Company
        fields = [
            'owner',
            'name',
            'description',
            'address',
            'city',
            'state',
            'contacto',
            'notes',
            'email',
            'url_corp',
            'feeds'
        ]


class ProviderForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = [
            'company',
            'name',
            'description',
            'address',
            'city',
            'state',
            'zipcode',
            'contacto',
            'notes',
            'email',
            'url_corp',
            'feeds'
        ]


class RestaurantForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = [
            'name',
            'description',
            'address',
            'city',
            'state',
            'contacto',
            'notes',
            'email',
            'url_corp',
            'feeds',
            'providers',
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
            'merma',

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
            'receta',
            'ingredient',
            'preparacion',
            'merma',
            'qty'

        ]

class NewUserForm(UserCreationForm):
   email = forms.EmailField(required=True)

   class Meta():
       model = get_user_model()
       fields = ('username','email','password1','password2','first_name','last_name')

   def save(self, commit=True):
       user = super(NewUserForm, self).save(commit=False)
       user.email = self.cleaned_data['email']
       if commit:
           user.save()
       return user

