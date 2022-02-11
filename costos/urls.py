from django.urls import path
from . import views



urlpatterns = [
      path('', views.index, name='index'),
      path('dashboard/', views.dashboard, name="dashboard"),
      path('forgot-password/', views.forgot_password, name="forgot_password"),
      path('register/', views.register, name="register"),
      path('prouser/', views.prouser_create, name="prouser_create"),
      path('login/', views.login, name="login"),
      path('company/', views.CompanyListView.as_view(), name="CompanyListView"),
      path('company/<int:pk>/', views.company_detail, name="company_detail"),
      path('company/add/', views.company_create, name="company_create"),
      path('provider/', views.ProviderListView.as_view(), name="ProviderListView"),
      path('provider/<int:pk>/', views.provider_detail, name="provider_detail"),
      path('provider/add/', views.provider_create, name="provider_create"),
      path('restaurant/', views.RestaurantListView.as_view() , name="restaurant"),
      path('restaurant/<int:pk>/', views.restaurant_detail, name="restaurant_detail"),
      path('restaurant/add/', views.restaurant_create, name="restaurant_create"),
      path('receta/', views.RecetaListView.as_view() , name="receta"),
      path('receta/<int:pk>/', views.receta_detail, name="receta_detail"),
      path('receta/add/', views.receta_create, name="receta_create"),
      path('ingredient/', views.IngredientListView.as_view(), name="IngredientListView"),
      path('ingredient/<int:pk>/', views.ingredient_detail, name="ingredient_detail"),
      path('ingredient/add/', views.ingredient_create, name="ingredient_create"),

]

