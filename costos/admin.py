from django.contrib import admin
from .models import User, Company, Restaurant, Provider, Ingredient, Receta, Steps

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)

admin.site.register(Company)
admin.site.register(Restaurant)
admin.site.register(Provider)
admin.site.register(Ingredient)
admin.site.register(Receta)
admin.site.register(Steps)