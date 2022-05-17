from django.urls import path
from . import views

urlpatterns = [
      # path('', views.index, name='index'),

      path('', views.HomeView.as_view(), name='home'),
      path('table/', views.recipe_decrease_scatter, name='recipe_table'),
      path('bar/', views.recipe_costbar, name='recipe_costbar'),
      path('table2/', views.ingredient_type_pie, name='ingredient_table'),
   #   path('image/', views.recipe_image, name='ingredient_image'),
      path('login/', views.login_request, name="login"),
      # path('accounts/logout/', name="logout"),
      # path('accounts/password_change/', name="password_change"),
      # path('accounts/password_change/done/', name="password_change_done"),
      # path('accounts/password_reset/', name="password_reset"),
      # path('accounts/password_reset/done/', name="password_reset_done"),
      # path('accounts/reset/<uidb64>/<token>/', name="password_reset_confirm"),
      # path('accounts/reset/done/', name="password_reset_complete"),
      path('dashboard/',views.dashboard,name="dashboard"),
      path('forgot_password/', views.forgot_password, name="forgot_password"),
      path('register/', views.register_request, name="register"),
      path('user/nuevo/', views.user_create, name="user_create"),
      path('accounts/login/', views.login_request, name="login"),
      path('companies/', views.CompanyListView.as_view(), name="company_list"),
      path('company/<int:pk>/', views.company_detail, name="company_detail"),
      path('company/add/', views.company_create, name="add_company"),
      path('company/<int:pk>/edit/', views.CompanyEditView.as_view(), name="company_edit"),
      path('providers/', views.ProviderListView.as_view(), name="provider_list"),
      path('provider/add/', views.ProviderCreateView.as_view(), name="provider_create"),
      path('provider/<int:pk>/edit/', views.ProviderEditView.as_view(), name="provider_edit"),
      path('provider/<int:pk>/', views.ProviderDetailView.as_view(), name="provider_detail"),
      path('provider/<int:pk>/ingredients/update/', views.provider_ingredient_update, name="provider_ingredient_update"),
      path('restaurants/', views.RestaurantListView.as_view() , name="restaurant_list"),
      path('es/restaurantes/', views.RestaurantListView.as_view(), name="restaurant_list"),
      path('restaurant/<int:pk>/', views.restaurant_detail, name="restaurant_detail"),
      path('restaurant/<int:pk>/edit/', views.RestaurantEditView.as_view(), name="restaurant_edit"),
      path('restaurant/add/', views.restaurant_create, name="restaurant_create"),
      path('recipes/', views.RecipeListView.as_view(), name="recipe_list"),
      path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name="recipe_detail"),
      path('recipe/add/', views.RecipeCreateView.as_view(), name="add_recipe"),
      path('recipe/add2/', views.Recipe2CreateView.as_view(), name="add_recipe2"),
      path('recipe/<int:pk>/update', views.RecipeEditView.as_view(), name="recipe_edit"),
      path('recipe/<int:pk>/step/update/', views.recipe_step_update, name="recipe_step_update"),
     # path('recipe/<int:pk>/step/create/', views.recipe_step_create, name="recipe_step_create"),
      #path('recipe/<int:pk>/step/<int:pk>/detail', views.recipe_step_detail, name="recipe_step_detail"),
     # path('es/recetas/', views.RecipeListView.as_view(), name="recipe_list"),
     #path('es/receta/<int:pk>/pasos/add/',views.steps_create, name="steps_create"),
     #path('es/receta/<int:pk>/steps/', views.StepListView.as_view(), name="steps_list"),
     # path('es/receta/<int:pk>/steps/<int:pk>/', views.steps_detail, name="steps_detail"),
     # path('recipe/<int:pk>/step/<int:pk>/', views.steps_detail, name="step_detail"),
      path('ingredients/', views.IngredientListView.as_view(), name="ingredient_list"),
      path('ingredient/<int:pk>/', views.ingredient_detail, name="ingredient_detail"),
      path('ingredient/<int:pk>/edit/', views.IngredientEditView.as_view(), name="ingredient_edit"),
      path('ingredient/add/', views.ingredient_create, name="ingredient_create"),


]


