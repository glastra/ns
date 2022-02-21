from django.urls import path
from django.urls import include, path
from . import views



urlpatterns = [
      path('', views.index, name='index'),
      # path('accounts/login/', name="login"),
      # path('accounts/logout/', name="logout"),
      # path('accounts/password_change/', name="password_change"),
      # path('accounts/password_change/done/', name="password_change_done"),
      # path('accounts/password_reset/', name="password_reset"),
      # path('accounts/password_reset/done/', name="password_reset_done"),
      # path('accounts/reset/<uidb64>/<token>/', name="password_reset_confirm"),
      # path('accounts/reset/done/', name="password_reset_complete"),
      path('dashboard/', views.dashboard, name="dashboard"),
      path('forgot_password/', views.forgot_password, name="forgot_password"),
      path('register/', views.register_request, name="register"),
      path('user/add/', views.user_create, name="user_create"),
      path('login/', views.login_request, name="login"),
      path('companies/', views.CompanyListView.as_view(), name="CompanyListView"),
      path('companies/<int:pk>/', views.company_detail, name="company_detail"),
      path('companies/add/', views.company_create, name="company_create"),
      path('providers/', views.ProviderListView.as_view(), name="ProviderListView"),
      path('providers/<int:pk>/', views.provider_detail, name="provider_detail"),
      path('providers/add/', views.provider_create, name="provider_create"),
      path('restaurants/', views.RestaurantListView.as_view() , name="restaurant_list"),
      path('restaurants/<int:pk>/', views.restaurant_detail, name="restaurant_detail"),
      path('restaurants/add/', views.restaurant_create, name="restaurant_create"),
      path('receta/', views.RecetaListView.as_view() , name="receta"),
      path('receta/<int:pk>/', views.receta_detail, name="receta_detail"),
      path('receta/add/', views.receta_create, name="receta_create"),
      path('ingredients/', views.IngredientListView.as_view(), name="ingredient_list"),
      path('ingredients/<int:pk>/', views.ingredient_detail, name="ingredient_detail"),
      path('ingredients/add/', views.ingredient_create, name="ingredient_create"),

]

