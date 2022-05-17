import os
import json

import matplotlib
import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
#import cufflinks as cf


from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory
from django.shortcuts import redirect, reverse, get_object_or_404
from django.views.generic import (TemplateView, CreateView, DetailView, FormView)
from django.views.generic.list import ListView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ingredient,  Recipe, Restaurant, Provider, Step, Company
from .forms import UserForm, RestaurantForm, IngredientForm, StepForm, ProviderForm, ProviderEditForm, CompanyEditForm, \
    RecipeEditForm, StepCreateForm
from .forms import RestaurantEditForm, NewUserForm, IngredientEditForm, ProviderIngredientsFormset, CompanyForm
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
# from plotly.offline import download_plotlyjs, init_notebook_mode,plot,iplot
# init_notebook_mode(connected=True)


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'


def index(request):
    return render(request, 'costos/index.html')


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    permission_required = 'costos.add_user'


def user_create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "costos/user_create.html",
                  context)


@login_required
def company_create(request):

    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_list')
    else:
        form = CompanyForm()
    context = {
        'form': form
    }
    return render(request, "costos/company_create.html", context)


class CompanyListView(ListView):
    model = Company
    template_name = 'company_list.html'


def company_detail(request, pk):
    company = Company.objects.get(pk=pk)

    if request.method == 'POST':
        Company.save

        return redirect('company_list')

    return render(request, 'costos/company_detail.html', {'company': company})


class CompanyEditView(SingleObjectMixin, FormView):

    model = Provider
    template_name = 'costos/company_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Company.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Company.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
         return CompanyEditForm(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes made'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('company_detail', kwargs={'pk': self.object.pk})




class ProviderCreateView(CreateView):
    model = Provider
    template_name = 'costos/provider_create.html'
    fields = [
        'name',
        'email',
        'description',

    ]

    def form_valid(self, form):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The provider has been added'
        )

        return super().form_valid(form)


class ProviderDetailView(DetailView):
    model = Provider
    template_name = 'costos/provider_detail.html'

    def form_valid(self, form):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The Provider has been added'
        )

        return super().form_valid(form)


class ProviderListView(ListView):
    model = Provider
    template_name = 'provider_list.html'


class ProviderEditView(SingleObjectMixin, FormView):

    model = Provider
    template_name = 'costos/provider_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Provider.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Provider.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
         return ProviderEditForm(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes made'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('provider_detail', kwargs={'pk': self.object.pk})


@login_required
def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()
    context = {
        'form': form
    }
    return render(request, "costos/restaurant_create.html", context)


def restaurant(request):
    return render(request, 'costos/restaurant.html')


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'


def restaurant_detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)

    if request.method == 'POST':
        restaurant.save

        return redirect('provider_list')

    return render(request, 'costos/restaurant_detail.html', {'restaurant': restaurant})


class RestaurantEditView(SingleObjectMixin, FormView):

    model = Provider
    template_name = 'costos/company_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Restaurant.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Restaurant.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
         return RestaurantEditForm(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes made'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('restaurant_detail', kwargs={'pk': self.object.pk})


def ingredient_create(request):
    chef = request.user
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.chef = chef
           # ingredient.qty2 = ingredient.qty1 * ingredient.decrease
            ingredient.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm()
    context = {
        'form': form
    }
    return render(request, "costos/ingredient_create.html", context)


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredient_list.html'


def ingredient_detail(request, pk):
    ingredient = Ingredient.objects.get(pk=pk)

    if request.method == 'POST':
        # temp = ingredient.qty1 - (ingredient.qty1 * ingredient.decrease)
        # print(temp)
        # if ingredient.qty2 != temp:
        #     ingredient.qty2 = ingredient.qty1 - (ingredient.qty1 * ingredient.decrease)

        Ingredient.save

        return redirect('ingredient_list')

    return render(request, 'costos/ingredient_detail.html', {'ingredient': ingredient})


class IngredientEditView(SingleObjectMixin, FormView):

    model = Ingredient
    template_name = 'costos/ingredient_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Ingredient.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Ingredient.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
         return IngredientEditForm( **self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes made on ingredient'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('ingredient_detail', kwargs={'pk': self.object.pk})


# def ingredient_type_pl(request):
#     arr_1 = np.random.randn(50,4)
#     df_1 = pd.DataFrame(arr_1, columns=['A','B','C','D'])
#     df_1.head()
#     df_1.plot()


def ingredient_type_pie(request):
    rategro = 0.0
    ratepro = 0.0
    ratefru = 0.0
    labels = 'grocery','protein','fruVer'
    label_type1 = 'protein'
    label_type2 = 'fruVer'
    label_type3 = 'grocery'
    # Creating color parameters
    colors = ("#4e73df", "#1cc88a", "#36b9cc")
    allint = Ingredient.objects.count()
    qs = Ingredient.objects.all().values('type').annotate(total=Count('id')).order_by('type')

    for q in qs:
        value = q['type']
        total = q['total']
        if value == label_type1:
            ratepro = total / allint
        if value == label_type2:
            ratefru = total / allint
        if value == label_type3:
            rategro = total / allint

    df = pd.DataFrame({'Name': ['grocery', 'protein','fruVer'],
                        'ing_type': [rategro, ratepro, ratefru]
                        }
                       )

    df = df.plot(kind='pie', y='ing_type', autopct='%1.0f%%', labels=labels, colors=colors)
    fname = 'ingredientepie.png'
    plt.savefig(os.path.join('costos/fig', fname))
    context = {'df': fname}
    return render(request, 'costos/ingredient_table.html', context)


class RecipeCreateView(CreateView):
    model = Recipe
    template_name = 'costos/recipe_create.html'
    fields = [
        'name',
        'portions',
        'items'
    ]


class Recipe2CreateView(CreateView):
        model = Recipe
        template_name = 'costos/recipe_create.html'
        fields = [
            'restaurant',
            'name',
            'portions',
        ]

    # def is_valid(self, form):
    #
    #     messages.add_message(
    #         self.request,
    #         messages.SUCCESS,
    #         'The Recipe has been added'
    #     )
    #     #response = super().form_valid()
    #     return super().form_valid()


class RecipeListView(ListView):
    model = Recipe


def recipe_decrease_scatter(request):

    qs = Recipe.objects.filter(is_complete=False)
    recipe = [{'Id': x.id, 'margin_error': x.margin_error, 'Portions': x.portions} for x in qs]
    #TS = datetime.now().strftime('%Y%m%d%H%M%S')
    fname = 'recipeerror.png'
    df = pd.DataFrame(recipe)

    json_records = df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)

    plt.figure()
    df.plot(x='margin_error', y='Portions', kind='scatter')
    plt.savefig(os.path.join('costos/fig', fname), bbox_inches='tight')
    #  plt.show()

    context = {'df': data}
    return render(request, 'costos/recipe_table.html', context)

def recipe_costbar(request):

    qs = Recipe.objects.filter(is_complete=False)

    recipe = [{'name': x.name, 'cost': float(x.cost.amount)} for x in qs]
    print(recipe)
    #TS = datetime.now().strftime('%Y%m%d%H%M%S')
    fname = 'recipecostbar.png'
    df = pd.DataFrame(recipe)

    json_records = df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)

   # plt.figure()
    df.plot(x='name', y='cost', kind='bar')
    plt.savefig(os.path.join('costos/fig', fname), bbox_inches='tight')
    #  plt.show()

    context = {'df': data}
    return render(request, 'costos/recipe_costbar.html', context)

#
# x = ['one', 'two', 'three', 'four', 'five']
#
# # giving the values against
# # each value at x axis
# y = [5, 24, 35, 67, 12]
# plt.bar(x, y)
#
# # setting x-label as pen sold
# plt.xlabel("pen sold")
#
# # setting y_label as price
# plt.ylabel("price")
# plt.title(" Vertical bar graph")



class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'costos/recipe_detail.html'

    def form_valid(self, form):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The Recipe has been added'
        )

        return super().form_valid(form)



class RecipeEditView(SingleObjectMixin, FormView):

    model = Recipe
    template_name = 'costos/recipe_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Recipe.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
         return RecipeEditForm(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes made on recipe'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.object.pk})



def steps_create(request):

    if request.method == 'POST':
        form = StepForm(request.POST)
        if form.is_valid():
            steps = form.save(commit=False)
            ing = steps.ingredient
            steps.cost_gmu = ing.price * ing.qty
            steps.cost_waste = (steps.cost_gmu * steps.error)/100
            steps.cost_total = (steps.cost_gmu * steps.qty) + steps.cost_waste
            steps.save()
            return redirect('recipe_detail')
    else:
        form = StepForm()
    context = {
        'form': form
    }
    return render(request, "costos/step_create.html", context)


def recipe_step_create(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe.save()
    if request.method == 'POST':
        recipe.save()
        form = StepCreateForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            steps = form.save(commit=False)
            steps.recipe = recipe

            # ing = steps.ingredient
            # steps.cost_gmu = ing.price * ing.qty
            # steps.cost_waste = (steps.cost_gmu * steps.error)/100
            # steps.cost_total = (steps.cost_gmu * steps.qty) + steps.cost_waste
            # recipe.cost = steps.cost_total
            steps.save()
            recipe.save()
            return redirect('steps_list', recipe.pk)
    else:
        form = StepCreateForm()
    context = {
        'form': form
    }
    return render(request, "costos/step_create.html", context)


def steps_detail(request, pk):
    steps = Step.objects.get(pk=pk)

    if request.method == 'POST':
        Step.save

        return redirect('steps_list')

    return render(request, 'costos/step_detail.html', {'steps': steps})


class StepListView(ListView):
    model = Step
    template_name = 'steps_list'


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="costos/login.html", context={"login_form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print('saved')
            messages.success(request, "Registration Successful")
            return redirect("login")
        messages.error(request, "Registration Unsuccessful")
    print('could not save')
    form = NewUserForm()
    return render(request=request, template_name="costos/register.html",
                  context={"register_form": form})


def logout_view(request):
    logout(request)

def forgot_password(request):
    return render(request, 'costos/forgot_password.html')


def dashboard(request):
    return render(request, 'costos/dashboard.html')



def recipe_step_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipestepformset = inlineformset_factory(Recipe, Step, fields=('ingredient', 'qty1', ))

    if request.method == "POST":
        print(request.POST)
        formset = recipestepformset(request.POST, instance=recipe)
     #   helper = StepFormSetHelper()
        if formset.is_valid():
            formset.save()
            return redirect('recipe_detail', recipe.pk)

    formset = recipestepformset(instance=recipe)

    return render(request, "costos/recipe_steps_update.html", {'formset': formset})





class ProviderIngredientsEditView(SingleObjectMixin, FormView):

    model = Provider
    template_name = 'costos/provider_ingredient_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Provider.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Provider.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return ProviderIngredientsFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
        self.request,
        messages.SUCCESS,
        'Changes made'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('provider_detail', kwargs={'pk': self.object.pk})


def provider_ingredients_edit(request, provider_pk, ingredient_pk):
    provider = get_object_or_404(Provider, pk=provider_pk)
    ingredient = get_object_or_404(Ingredient, pk=ingredient_pk, provider=provider)

    IngredientFormSet = inlineformset_factory(
        Provider,  # parent model
        Ingredient,  # base model
        fields=('name', 'description'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=provider)
        formset = IngredientFormSet(request.POST, instance=provider)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Provider and ingredients saved with success!')
            return redirect('provider_detail', provider.pk)

        else:
            form = ProviderForm(instance=provider)
            formset = IngredientFormSet(instance=provider)

        return render(request, 'costos/provider_ingredient_update.html', {
            'provider': provider,
            'ingredient': ingredient,
            'form': form,
            'formset': formset
        })
    
    
def provider_ingredient_update(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    provider_ingredient_formset = inlineformset_factory(Provider, Ingredient, fields=('name', 'presentation','price',
                                                                                      'qty1', 'decrease', 'qty2'))

    if request.method == "POST":
        print(request.POST)
        formset = provider_ingredient_formset(request.POST, instance=provider)
        if formset.is_valid():
            formset.save()

            return redirect('provider_detail', provider.pk)

    formset = provider_ingredient_formset(instance=provider)

    return render(request, "costos/provider_ingredient_update.html", {
        'provider': provider,
        'formset': formset

    })
