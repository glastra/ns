from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.forms import ModelForm
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic.list import ListView
from django.shortcuts import render
from .models import Ingredient,  Receta, Restaurant, Provider
from .forms import ProviderForm, UserForm,  RestaurantForm, IngredientForm, RecetaForm, NewUserForm, StepsForm

from formtools.wizard.views import WizardView

# Create your views here.
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


class ProviderListView(LoginRequiredMixin, ListView):
    model = Provider


def provider_create(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('provider_list')
    else:
        form = ProviderForm()
    context = {
        'form': form
    }
    return render(request, "costos/provider_create.html",
                  context)


def restaurant_create(request):

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.manager = request.user
            restaurant.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm()
    context = {
        'form': form
    }
    return render(request, "costos/restaurant_create.html", context)


def ingredient_create(request):

    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.chef = request.user
            ingredient.save()
            return redirect('ingredient_list')
    else:
        form = IngredientForm()
    context = {
        'form': form
    }
    return render(request, "costos/ingredient_create.html",context)


class IngredientListView(ListView):
    model = Ingredient


def ingredient_detail(request, pk):
    ingredient = Ingredient.objects.get(pk=pk)

    if request.method == 'POST':
        Ingredient.save

        return redirect('ingredient_list')

    return render(request, 'costos/ingredient_detail.html', {'ingredient': ingredient})


class ProviderListView(ListView):
    model = Provider


def provider_detail(request, pk):
    provider = Provider.objects.get(pk=pk)

    if request.method == 'POST':
        Provider.save

        return redirect('provider_list')

    return render(request, 'costos/provider_detail.html', {'provider': provider})


def provider_create(request):
    form = ProviderForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "costos/provider_create.html",
                  context)


def restaurant(request):
    return render(request, 'costos/restaurant.html')


class RestaurantListView(ListView):
    model = Restaurant


def restaurant_detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)

    if request.method == 'POST':
        Restaurant.save

        return redirect('provider_list')

    return render(request, 'costos/restaurant_detail.html', {'restaurant': restaurant})


class RecetaListView(ListView):
    model = Receta


class RecetaCreateForm(ModelForm):

    class Meta:
        model = Receta
        exclude = ['restaurant', 'items']
        fields = [
            'name',
            'description',
            'portions',
        ]

    def __init__(self, request, *args, ** kwargs):
        super(RecetaCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, **kwargs):

        r_create_form = super(Receta, self).save(commit=False)
        r_create_form.restaurant = 'NS restaurante'
        if commit:
            r_create_form.save()
        return r_create_form




class RecetaAddView(LoginRequiredMixin, View):

    model = Receta

    def get(self, request, *args, **kwargs):
        form = RecetaCreateForm(request)
        context = {'form': form}
        return render(request, 'costos/receta_create.html', context)

    def post(self, request, *args, **kwargs):
        form = RecetaCreateForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect(reverse('costos:index'))

def receta(request):
    return render(request, 'costos/receta.html')


def receta_create(request):
    form = RecetaForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "costos/receta_create.html",
                  context)


def receta_detail(request, pk):
    receta = Receta.objects.get(pk=pk)

    if request.method == 'POST':
        receta.save

        return redirect('recetalist')

    return render(request, 'costos/restaurant_detail.html', {'restaurant': restaurant})


def steps_create(request):

    if request.method == 'POST':
        form = StepsForm(request.POST)
        if form.is_valid():
            steps = form.save(commit=False)
            ing = steps.ingredient
            steps.cost_gmu = ing.price * ing.qty
            steps.cost_waste = (steps.cost_gmu * steps.error)/100
            steps.cost_total = (steps.cost_gmu * steps.qty) + steps.cost_waste
            steps.save()
            return redirect('index')
    else:
        form = StepsForm()
    context = {
        'form': form
    }
    return render(request, "costos/steps_create.html", context)


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
                return redirect("index")
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
            return redirect("index")
        messages.error(request, "Registration Unsuccessful")
    print('could not save')
    form = NewUserForm()
    return render(request=request, template_name="costos/register.html",
                  context={"register_form": form})


def logout_view(request):
    logout(request)

def forgot_password(request):
    return render(request, 'costos/forgot_password.html')

#
# class CompanyListView(ListView):
#     model = Company
#
#
# def company_create(request):
#     form = CompanyForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#     context = {
#         'form': form
#     }
#     return render(request, "costos/company_create.html",
#                   context)
#
#
# def company_detail(request, pk):
#     company = Company.objects.get(pk=pk)
#
#     if request.method == 'POST':
#         Provider.save()
#
#         return redirect('provider_list')
#     return render(request, 'costos/company_detail.html', {'company': company})


def dashboard(request):
    return render(request, 'costos/dashboard.html')
