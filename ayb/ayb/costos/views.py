from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from .models import Ingredient
from .models import Company
from .models import Restaurant
from .models import Provider
from .models import Receta
from django.shortcuts import render
from .forms import ProviderForm

# Create your views here.



def index(request):
    return render(request, 'costos/index.html')

class ProviderListView(PermissionRequiredMixin, ListView):
   model = Provider
   permission_required = 'costos.add_provider'

def provider_create(request):
    form = ProviderForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "costos/provider_create.html",
    context)
