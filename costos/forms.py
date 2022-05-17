from crispy_forms.bootstrap import PrependedText
from django import forms
from django_quill.forms import QuillFormField
from .models import  Restaurant, Provider, Ingredient, Recipe, Step, Company
from django.forms import ModelForm, HiddenInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Hidden
from crispy_forms.bootstrap import PrependedText
from django_countries.widgets import CountrySelectWidget


class QuillFieldForm(forms.Form):
    content = QuillFormField()

RecipeStepFormset = inlineformset_factory(Recipe, Step, fields=('preparation', 'qty1', 'qty2', 'ingredient',))

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
            'phone',

        ]


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'name',
            'description',
            'owner',
            'identification',
            'country',
            'extra_street',
            'street',
            'city',
            'state',


        ]
        widgets = {'country': CountrySelectWidget()}


class CompanyEditForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'name',
            'description',
            'owner',
            'identification',
            'country',
            'extra_street',
            'street',
            'city',
            'state',

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
            'zipcode',
            'contact',
            'email',
            'web',
        ]


class ProviderEditForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = [
            'name',
            'description',
            'extra_street',
            'street',
            'city',
            'state',
            'zipcode',
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
            'country',
            'extra_street',
            'street',
            'city',
            'state',
            'chef',

        ]
        widgets = {'country': CountrySelectWidget()}


class RestaurantEditForm(forms.ModelForm):

    class Meta:
        model = Restaurant
        fields = [
            'name',
            'description',
            'country',
            'extra_street',
            'street',
            'city',
            'state',
            'chef',

        ]


class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        exclude = ['qty2', ]
        fields = [

            'provider',
            'name',
            'description',
            'presentation',
            'type',
            'price',
            'qty1',
            'decrease',

        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            PrependedText('price', '$')
             )


class IngredientEditForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        exclude = ['qt2']
        fields = [
            'provider',
            'description',
            'presentation',
            'type',
            'price',
            'qty1',
            'decrease',

        ]

    def __init__(self, *args, **kwargs):
        super(IngredientEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            PrependedText('price', '$')
            )

    # def save(self, commit=True, **kwargs):
    #     # i_create_form = super(Ingredient, self).save(commit=True)
    #     # if i_create_form.qyt2 > i_create_form.qty1:
    #     #     i_create_form.qyt2 = i_create_form.qty1
    #     # if not commit:
    #     #     raise NotImplementedError("Can't create ingredient  without config save")
    #
    #     i_create_form.save()
    #     return i_create_form


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'name',
            'description',
            'portions',
        ]


class RecipeCreateForm(ModelForm):

    class Meta:
        model = Recipe
        exclude = ['restaurant']
        fields = [
            'name',
            'description',
            'portions',
            'margin_error',
        ]

    def __init__(self, request, *args, ** kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_id = 'id-recipeCreateForm'
        self.helper.form_tag = False

    def save(self, commit=True, **kwargs):
        r_create_form = super(Recipe, self).save(commit=True)
        r_create_form.restaurant = 'NS restaurant'

        if not commit:
            raise NotImplementedError("Can't create recipe without an ingredient")

        r_create_form.save()
        return r_create_form


class RecipeEditForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ['items', 'chef']
        fields = [
            'restaurant',
            'name',
            'description',
            'portions',
            'margin_error',
            'menu_price',
            'is_complete',
            'is_track',

        ]
        widgets = {'description': QuillFieldForm()}

    # def __init__(self, *args, **kwargs):
    #     super(RecipeEditForm, self).__init__(*args, **kwargs)
    #     if self.instance.pk:
    #         self.fields['items'].initial = \
    #             self.instance.items_set.all().select_subclasses()
    #
    # def save(self, commit=True):
    #     recipe = super(RecipeEditForm, self).save(commit=False)
    #     recipe.save()
    #     # recipe.items_set = self.cleaned_data['items']
    #     # self.save_m2m()
    #     return recipe


    # def duplicate(self):
    #     recipe = Recipe.objects.get(pk=pkofquiziwanttocopy)
    #     quiz.pk = None
    #     quiz.save()
    #     old_quiz = Quiz.objects.get(pk=pkofquiziwanttocopy)
    #
    #     quiz.question_set = old_quiz.question_set.all()

class StepForm(forms.ModelForm):

    class Meta:
        model = Step
        exclude = ['decrease', 'qty2']
        fields = [
            'ingredient',
            'qty1',
            'qty2',
            'decrease',
            'preparation',
            'duration',
        ]


class StepCreateForm(forms.ModelForm):

    class Meta:
        model = Step
        exclude = ['qty2']
        fields = [
            'ingredient',
            'qty1',
            'qty2',
            'decrease',
            'preparation',
            'duration',
        ]



# class StepFormSetHelper(FormHelper):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.form_method = 'post'
#         self.layout = Layout(
#             'ingredient',
#             'qty1',
#         )
#         self.render_required_fields = True


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

