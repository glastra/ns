from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _



# create a pro user model
class ProUser(models.Model):
    # declare pro user attributes
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    account_id = models.CharField(max_length=10)
    phone = models.CharField(max_length=12)
    country = models.CharField(max_length=12)
    address = models.CharField(_('address'), max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    zipCode = models.CharField(_('zipCode'), max_length=100, blank=True)
    contacto = models.CharField(_('contacto'), max_length=100, blank=True)
    notes = models.CharField(_('notes'), max_length=250, blank=True)
    verified = models.BooleanField(default=False, verbose_name=_('Verified'))
    is_pro = models.BooleanField(default=False)


    def __str__(self):
        return self.user.get_full_name()
