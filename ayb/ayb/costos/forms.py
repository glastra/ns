from django import forms
from .models import ProUser
from .models import Company
from .models import Restaurant
from .models import Provider
from .models import Ingredient
from .models import Receta
from .models import Steps


class ProUserForm(forms.ModelForm):
    class Meta:
        model = ProUser
        fields = [
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