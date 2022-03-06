from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, inlineformset_factory, modelformset_factory
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, get_object_or_404
from django.views.generic import (TemplateView, CreateView, DetailView, FormView)
from django.views.generic.list import ListView
from django.shortcuts import render
from .models import Ingredient,  Receta, Restaurant, Provider, Steps
from .forms import UserForm,  RestaurantForm, IngredientForm, StepsForm, ProviderForm, RecetaForm
from .forms import RecetaStepsFormset, NewUserForm, IngredientEditForm, ProviderIngredientsFormset

from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from formtools.wizard.views import WizardView


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


class ProviderCreateView(CreateView):
    model = Provider
    template_name = 'costos/provider_create.html'
    fields = [
        'name',
        'description',
        'email',

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


def restaurant(request):
    return render(request, 'costos/restaurant.html')


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'


def restaurant_detail(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)

    if request.method == 'POST':
        Restaurant.save

        return redirect('provider_list')

    return render(request, 'costos/restaurant_detail.html', {'restaurant': restaurant})


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
    return render(request, "costos/ingredient_create.html", context)


class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredient_list.html'


def ingredient_detail(request, pk):
    ingredient = Ingredient.objects.get(pk=pk)

    if request.method == 'POST':
        Ingredient.save

        return redirect('ingredient_list')

    return render(request, 'costos/ingredient_detail.html', {'ingredient': ingredient})


class RecetaCreateView(CreateView):
    model = Receta
    template_name = 'costos/receta_create.html'
    fields = [
        'name',
        'portions',
        'chef',
        'restaurant',
        'errormargin',
        'items'
    ]

    def is_valid(self, form):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The receta has been added'
        )

        return super().is_valid(form)


class RecetaListView(ListView):
    model = Receta


class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'costos/receta_detail.html'

    def form_valid(self, form):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'The receta has been added'
        )

        return super().form_valid(form)


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


def steps_detail(request, pk):
    steps = Steps.objects.get(pk=pk)

    if request.method == 'POST':
        Steps.save

        return redirect('steps_list')

    return render(request, 'costos/steps_detail.html', {'steps': steps})



class StepListView(ListView):
    model = Steps
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


class RecetaStepsEditView(SingleObjectMixin, FormView):

    model = Receta
    template_name = 'costos/receta_steps_update.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Receta.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Receta.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return RecetaStepsFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes made'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('receta_detail', kwargs={'pk': self.object.pk})


def receta_steps_update(request, pk):
    obj = get_object_or_404(Receta, pk=pk)
   # obj = Receta.objects.get(pk=pk)
    form = RecetaForm()
    RecetaStepsFormset = modelformset_factory(Steps, form=StepsForm, extra=2)
    qs = obj.items.all()
    formset = RecetaStepsFormset(request.POST or None, queryset=qs)
    context = {
        'form' : form,
        'formset': formset,
        'object' : obj
    }
    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.receta = parent
            child.save()
        context['message'] = 'Data saved'
    return render(request, "costos/receta_steps_update.html", context)




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
         return IngredientEditForm(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Changes made'
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('ingredient_detail', kwargs={'pk': self.object.pk})


class ProviderIngredientsEditView(SingleObjectMixin, FormView):

    model = Provider
    template_name = 'costos/provider_ingredients_edit.html'

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


def provider_ingredients_edit(request, provider_pk, ingredient_pk, *args, **kwargs):
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

        return render(request, 'costos/provider_ingredients_edit.html', {
            'provider': provider,
            'ingredient': ingredient,
            'form': form,
            'formset': formset
        })