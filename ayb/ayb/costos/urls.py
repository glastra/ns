from django.urls import path
from . import views


urlpatterns = [
      path('',views.index),
      path('prouser/add/', views.prouser_create, name="add_prouser"),
      path('provider/', views.ProviderListView.as_view(), name="ProviderListView"),
      path('provider/add/', views.provider_create, name="add_provider"),
      path('company/add/', views.company_create, name="add_company"),
      path('restaurant/add/', views.restaurant_create, name="add_restaurant"),
]