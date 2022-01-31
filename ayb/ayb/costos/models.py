from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
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


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('name'), max_length=250)
    description = models.CharField(_('description'), max_length=250, blank=True)
    address = models.CharField(_('address'), max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    zipCode = models.CharField(_('zipCode'), max_length=100, blank=True)
    contacto = models.CharField(_('contacto'), max_length=100, blank=True)
    notes = models.CharField(_('notes'), max_length=250, blank=True)
    email = models.EmailField(_('email'), max_length=70, blank=True)
    phone = models.CharField(_('phone'), max_length=250, blank=True)
    url_corp = models.CharField(_('url'), max_length=250, blank=True)
    feeds = models.CharField(_('feeds'), max_length=250, blank=True)
    owner = models.ForeignKey(get_user_model(), related_name='company_owner', null=True, on_delete=models.SET_NULL)
    restaurants = models.ManyToManyField('Restaurant')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Company:detail', kwargs={
            'id': self.id
        })


class Provider(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(_('name'), max_length=250)
        description = models.CharField(_('description'), max_length=250, blank=True)
        address = models.CharField(_('address'), max_length=100, blank=True)
        city = models.CharField(_('city'), max_length=100, blank=True)
        state = models.CharField(_('state'), max_length=100, blank=True)
        zipcode = models.CharField(_('zipcode'), max_length=100, blank=True)
        contacto = models.CharField(_('contacto'), max_length=100, blank=True)
        notes = models.CharField(_('notes'), max_length=250, blank=True)
        email = models.EmailField(max_length=70, blank=True, unique=True)
        phone = models.CharField(_('phone'), max_length=250, blank=True)
        url_corp = models.CharField(_('url'), max_length=250, blank=True)
        feeds = models.CharField(_('feeds'), max_length=250, blank=True)
        company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
#        ingredients = models.ManyToManyField('Ingredient')

        def __str__(self):
            return self.name

        def get_absolute_url(self):
            return reverse('Provider:detail', kwargs={
                'id': self.id
            })

class Restaurant(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(_('name'), max_length=250)
        description = models.CharField(_('description'), max_length=250, blank=True)
        address = models.CharField(_('address'), max_length=250, blank=True)
        city = models.CharField(_('city'), max_length=100, blank=True)
        state = models.CharField(_('state'), max_length=100, blank=True)
        zipCode = models.CharField(_('zipCode'), max_length=100, blank=True)
        contacto = models.CharField(_('contacto'), max_length=100, blank=True)
        notes = models.CharField(_('notes'), max_length=250, blank=True)
        email = models.EmailField(_('email'), max_length=70, blank=True)
        phone = models.CharField(_('phone'), max_length=250, blank=True)
        url_corp = models.CharField(_('url'), max_length=250, blank=True)
        feeds = models.CharField(_('feeds'), max_length=250, blank=True)
        chefs = models.ManyToManyField(get_user_model(), related_name='restaurant_chef')
        manager = models.ForeignKey(get_user_model(), related_name='restaurant_manager', on_delete=models.CASCADE)
        providers = models.ManyToManyField(Provider)

        def __str__(self):
            return self.name

        def get_absolute_url(self):
            return reverse('Restaurant:detail', kwargs={
                'id': self.id
            })

