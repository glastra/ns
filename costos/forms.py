from django import forms
from .models import ProUser
from .models import Company
from .models import Restaurant
from .models import Provider
from .models import Ingredient
from .models import Receta
from .models import Steps
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ProUserForm(forms.ModelForm):
    class Meta:
        model = ProUser
        fields = [
            'user',
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
            'name',
            'description',
            'presentation',
            'type',
            'price',
            'qty',
            'merma'

        ]

class RecetaForm(forms.ModelForm):

    class Meta:
        model = Receta
        fields = [
            'chef',
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
            'preparacion',
            'merma',
            'qty'

        ]

class RegistrationForm(UserCreationForm):
   email = forms.EmailField(required=True)
   class Meta():
       model = User
       fields = ('username','email','password1','password2','first_name','last_name')

   def save(self, commit=True):
       user = super(RegistrationForm, self).save(commit=False)
       user.email = self.cleaned_data['email']
       if commit:
           user.save()
       return user

   #
   # class Meta:
	#     model = User
	#     fields = [
   #          'username',
   #          'first_name',
   #          'last_name',
   #          'email',
   #          'password1',
   #          'password2'
   #      ]