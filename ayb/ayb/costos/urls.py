from django.urls import path
from . import views


urlpatterns = [
      path('',views.index),
      path('provider/', views.ProviderListView.as_view(), name="ProviderListView"),
      path('provider/add/', views.provider_create, name="add_provider"),
]