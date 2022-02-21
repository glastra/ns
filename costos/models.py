from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# create a pro user model
class User(AbstractUser):
    # declare pro user attributes
    account_id = models.CharField(max_length=10)
    phone = models.CharField(max_length=12)
    country = models.CharField(max_length=12)
    address = models.CharField(_('address'), max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    zip_code = models.CharField(_('zip code'), max_length=100, blank=True)
    contacto = models.CharField(_('contacto'), max_length=100, blank=True)
    notes = models.CharField(_('notes'), max_length=250, blank=True)
    verified = models.BooleanField(default=False, verbose_name=_('Verified'))
    is_pro = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()


class Company(models.Model):

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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Provider:detail', kwargs={
                'id': self.id
            })

class Restaurant(models.Model):

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
    manager = models.ForeignKey(get_user_model(), related_name='restaurant_manager', on_delete=models.CASCADE, null=True)
    providers = models.ManyToManyField(Provider)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Restaurant:detail', kwargs={
               'id': self.id
            })

class Ingredient(models.Model):

    GRAM = "gram"
    UNIT = "unit"
    MILLILITER = "milliliter"
    KILOGRAM = "kilogram"

    PRESENTATION_CHOICES = [
        (GRAM, "Gram"),
        (UNIT, "Unit"),
        (MILLILITER, "Milliliter"),
        (KILOGRAM, "Kilogram")
    ]

    GROCERY = "grocery"
    PROTEIN = "protein"
    FRUVER = "fruVer"
    CATEGORY_CHOICES = [
        (GROCERY, "Grocery"),
        (PROTEIN, "Protein"),
        (FRUVER, "FruVer")
    ]

    name = models.CharField(_('name'), max_length=250)
    type = models.CharField(_('type'), max_length=50, choices=CATEGORY_CHOICES, default=GROCERY)
    presentation = models.CharField(_('presentation'), max_length=50, choices=PRESENTATION_CHOICES, default=GRAM)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(_('description'), max_length=999)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    qty = models.DecimalField(max_digits=20, decimal_places=10)
    merma = models.DecimalField(max_digits=10, decimal_places=6, default=0.01)

    provider = models.ForeignKey(Provider, related_name='ingredient_provider', on_delete=models.CASCADE)
    chef = models.ForeignKey(get_user_model(), related_name='ingredient_chef', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Ingredient:detail', kwargs={
            'id': self.id
        })



class Receta(models.Model):

    name = models.CharField(_('name'), max_length=100)
    description = models.CharField(_('description'), max_length=250, blank=True)
    isComplete = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=20, decimal_places=10)
    portions = models.DecimalField(max_digits=20, decimal_places=10, default=1.0)
    mpcost = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    prepacost = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    portioncost = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    mpestablish = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    errormargin = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    realratemp = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    saleprice = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    menuprice = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    realsaleprice = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    taxportion = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=models.SET_NULL)
    items = models.ManyToManyField(Ingredient, through='Steps', through_fields=('receta', 'ingredient'))
    chef = models.ForeignKey(get_user_model(), related_name='receta_chef', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Receta:detail', kwargs={
            'id': self.id
        })

class Steps(models.Model):

    qty = models.DecimalField(_('qty'), max_digits=20,decimal_places=10)
    preparacion = models.CharField(_('preparation'), max_length=250)
    merma = models.DecimalField(_('merma'), max_digits=10,decimal_places=6)

    receta = models.ForeignKey(Receta,related_name='steps_receta',on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,related_name='steps_ingredient',on_delete=models.CASCADE)

    def __str__(self):
        return self.preparacion

    def get_absolute_url(self):
        return reverse('Step:detail', kwargs={
            'id': self.id
       })

