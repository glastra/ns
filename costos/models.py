from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


# create a Place model
class Place(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    street = models.CharField(_('street'), max_length=100, blank=True)
    extra_street = models.CharField(_('street'),  max_length=100, blank=True)
    city = models.CharField(_('city'),  max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    zip_code = models.CharField(_('zip code'), max_length=100, blank=True)
    contacto = models.CharField(_('contacto'),  max_length=100, blank=True)
    phone = models.CharField(_('phone'), max_length=12)
    notes = models.CharField(_('notes'), max_length=250, blank=True)
    verified = models.BooleanField(default=False,  verbose_name=_('Verified'))
    def __str__(self):
        return self.name


# create a pro user model
class User(AbstractUser, Place):
    # declare pro user attributes
    account_id = models.CharField(max_length=10)
    user_phone = models.CharField(max_length=12)
    is_pro = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name()


class Company(Place):

    co_name = models.CharField(_('company_name'), max_length=250)
    description = models.CharField(_('company_description'), max_length=250, blank=True)
    email = models.EmailField(_('company_email'), max_length=70, blank=True)
    url_corp = models.CharField(_('company_web'), max_length=250, blank=True)
    feeds = models.CharField(_('company_feeds'), max_length=250, blank=True)
    owner = models.ForeignKey(get_user_model(), related_name='company_owner', null=True, on_delete=models.SET_NULL)
    restaurants = models.ManyToManyField('Restaurant', related_name='company_restaurants')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Company:detail', kwargs={
            'id': self.id
        })


class Provider(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(_('description'), max_length=250, blank=True)
    email = models.EmailField(_('email'),max_length=70, blank=True, unique=True)
    url_corp = models.CharField(_('web'), max_length=250, blank=True)
    feeds = models.CharField(_('feeds'), max_length=250, blank=True)
    country = models.CharField(max_length=100)
    street = models.CharField(_('street'), max_length=100, blank=True)
    extra_street = models.CharField(_('street'), max_length=100, blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    zip_code = models.CharField(_('zip code'), max_length=100, blank=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL, related_name='provider_companies')
    contacto = models.CharField(_('contacto'), max_length=100, blank=True)
    phone = models.CharField(_('phone'), max_length=12)
    notes = models.CharField(_('notes'), max_length=250, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Provider:detail', kwargs={
                'id': self.id
            })

class Restaurant(Place):

    restaurant_name = models.CharField(_('restaurant_name'), max_length=250)
    description = models.CharField(_('restaurant_description'), max_length=250, blank=True)
    email = models.EmailField(_('restaurant_email'), max_length=70, blank=True)
    url_corp = models.CharField(_('restaurant_web'), max_length=250, blank=True)
    feeds = models.CharField(_('restaurant_feeds'), max_length=250, blank=True)
    chefs = models.ManyToManyField(get_user_model(), related_name='restaurant_chefs')
    manager = models.ForeignKey(get_user_model(), related_name='restaurant_manager', on_delete=models.CASCADE, null=True)
    providers = models.ManyToManyField(Provider, related_name='restaurant_providers')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Restaurant:detail', kwargs={
               'id': self.id
            })


# create a profile
class UserProfile(User):
    # declare user profile
    profile_restaurant = models.OneToOneField(Restaurant, related_name='profile_restaurant', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


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

    name = models.CharField(_('ingredient_name'), max_length=250)
    type = models.CharField(_('type'), max_length=50,choices=CATEGORY_CHOICES, default=GROCERY)
    presentation = models.CharField(_('presentation'), max_length=50, choices=PRESENTATION_CHOICES, default=GRAM)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(_('ingredient_description'), max_length=999)
    price = models.DecimalField(_('ingredient_price'), max_digits=20, decimal_places=10)
    qty = models.DecimalField(_('ingredient_quantity'), max_digits=20, decimal_places=10)
    merma = models.DecimalField(_('ingredient_error'), max_digits=10, decimal_places=6, default=0.01)
    provider = models.ForeignKey(Provider, related_name='ingredient_provider', on_delete=models.CASCADE)
    chef = models.ForeignKey(get_user_model(), related_name='ingredient_chef', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Ingredient:detail', kwargs={
            'id': self.id
        })



class Receta(models.Model):

    name = models.CharField(_('receta_name'), max_length=100)
    description = models.CharField(_('receta_description'), max_length=250, blank=True)
    isComplete = models.BooleanField(_('receta_copmlete'),default=False)
    cost = models.DecimalField(_('receta_cost'),max_digits=20, decimal_places=10)
    portions = models.DecimalField(_('receta_portions'),max_digits=20, decimal_places=10, default=1.0)
    mpcost = models.DecimalField(_('receta_mpcost'),max_digits=20, decimal_places=10, default=0.0)
    prepacost = models.DecimalField(_('receta_prep_cost'),max_digits=20, decimal_places=10, default=0.0)
    portioncost = models.DecimalField(_('receta_p_cost'),max_digits=20, decimal_places=10, default=0.0)
    mpestablish = models.DecimalField(_('receta_e_cost'),max_digits=20, decimal_places=10, default=0.0)
    errormargin = models.DecimalField(_('receta_error_margin'),max_digits=20, decimal_places=10, default=0.01)
    realratemp = models.DecimalField(_('receta_real_price'),max_digits=20, decimal_places=10, default=0.0)
    saleprice = models.DecimalField(_('receta_sale_price'),max_digits=20, decimal_places=10, default=0.0)
    menuprice = models.DecimalField(_('receta_menu_price'),max_digits=20, decimal_places=10, default=0.0)
    realsaleprice = models.DecimalField(_('receta_r_price'),max_digits=20, decimal_places=10, default=0.0)
    taxportion = models.DecimalField(_('receta_tax'),max_digits=20, decimal_places=10,default=0.0)
    duration = models.DurationField(_('receta_duration'), default="00:01:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=models.SET_NULL, related_name='receta_restaurant')
    items = models.ManyToManyField(Ingredient, through='Steps', through_fields=('receta', 'ingredient'))
    chef = models.ForeignKey(get_user_model(), related_name='receta_chef', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Receta:detail', kwargs={
            'id': self.id
        })

class Steps(models.Model):

    qty = models.DecimalField(_('step_qty'), max_digits=20,decimal_places=10, default=1.0)
    preparacion = models.CharField(_('step_preparation'), max_length=250)
    merma = models.DecimalField(_('step_error'), max_digits=10,decimal_places=6,  default=0.001)
    receta = models.ForeignKey(Receta, related_name='steps_receta', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='steps_ingredient', on_delete=models.CASCADE)
    duration = models.DurationField(_('step_duration'), default="00:01:00")

    def __str__(self):
        return self.preparacion

    def get_absolute_url(self):
        return reverse('Step:detail', kwargs={
            'id': self.id
       })

