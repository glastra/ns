from django.contrib import admin
from .models import User, Restaurant, Provider, Ingredient, Receta, Steps, Profile


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


admin.site.register(Restaurant)
admin.site.register(Provider)
admin.site.register(Ingredient)
admin.site.register(Receta)
admin.site.register(Steps)
admin.site.register(Profile)
