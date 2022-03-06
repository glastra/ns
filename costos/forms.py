from django import forms
from .models import  Restaurant, Provider, Ingredient, Receta, Steps
from django.forms import ModelForm, HiddenInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Hidden


RecetaStepsFormset = inlineformset_factory(Receta, Steps, fields=('preparation', 'qty','ingredient',))

ProviderIngredientsFormset = inlineformset_factory(
    Provider,
    Ingredient,
    can_delete=True,
    extra=3,
    fields=('name', 'price', 'type','presentation',)
)

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


class IngredientEditForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = [
            'provider',
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


class RecetaCreateForm(ModelForm):

    class Meta:
        model = Receta
        exclude = ['restaurant', 'items']
        fields = [
            'name',
            'description',
            'portions',
            'errormargin',
        ]

    def __init__(self, request, *args, ** kwargs):
        super(RecetaCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-recetaCreateForm'
        self.helper.form_tag = False

    def save(self, commit=True, **kwargs):
        r_create_form = super(Receta, self).save(commit=False)
        r_create_form.restaurant = 'NS restaurante'
        if commit:
            r_create_form.save()
        return r_create_form





class StepsForm(forms.ModelForm):

    class Meta:
        model = Steps
        fields = [
            'receta',
            'ingredient',
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

