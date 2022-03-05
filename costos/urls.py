from django.urls import path
from . import views

urlpatterns = [
      # path('', views.index, name='index'),
      path('', views.HomeView.as_view(), name='home'),
      path('login/', views.login_request, name="login"),
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
      path('user/nuevo/', views.user_create, name="user_create"),
      path('accounts/login/', views.login_request, name="login"),
      # path('companias/', views.CompanyListView.as_view(), name="CompanyListView"),
      # path('companias/<int:pk>/', views.company_detail, name="company_detail"),
      # path('companias/add/', views.company_create, name="company_create"),
      path('providers/', views.ProviderListView.as_view(), name="ProviderListView"),
      path('provider/<int:pk>/', views.provider_detail, name="provider_detail"),
      path('provider/add/', views.provider_create, name="provider_create"),
      path('restaurants/', views.RestaurantListView.as_view() , name="restaurant_list"),
      path('restaurant/<int:pk>/', views.restaurant_detail, name="restaurant_detail"),
      path('restaurant/add/', views.restaurant_create, name="restaurant_create"),
      path('recetas/', views.RecetaListView.as_view() , name="RecetaViewList"),
      path('receta/<int:pk>/', views.RecetaDetailView.as_view(), name="receta_detail"),
      path('receta/<int:pk>/steps/edit/', views.RecetaStepsEditView.as_view(), name="receta_steps_edit"),
      path('receta/add/', views.RecetaCreateView.as_view(), name="add_receta"),
      path('steps/add/', views.steps_create, name="steps_create"),
      path('steps/', views.StepListView.as_view(), name="steps_list"),
      path('steps/<int:pk>/', views.steps_detail, name="steps_detail"),
      path('ingredients/', views.IngredientListView.as_view(), name="IngredientViewList"),
      path('ingredient/<int:pk>/', views.ingredient_detail, name="ingredient_detail"),
     # path('ingredient/<int:pk>/steps/edit/', views.IngredientStepsEditView.as_view(), name="ingredient_steps_edit"),
      path('ingredient/add/', views.ingredient_create, name="ingredient_create"),


]

