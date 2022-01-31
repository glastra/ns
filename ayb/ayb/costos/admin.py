from django.contrib import admin
from .models import ProUser
from .models import Company
from .models import Restaurant
from .models import Provider
# Register your models here.
admin.site.register(ProUser)
admin.site.register(Company)
admin.site.register(Restaurant)
admin.site.register(Provider)