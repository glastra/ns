from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


# create a pro user model
class User(AbstractUser):

    account_id = models.CharField(_('Account'), max_length=10)
    phone = models.CharField(_('Phone'), max_length=12)
    verified = models.BooleanField(default=False,  verbose_name=_('Verified'))

    def __str__(self):
        return self.get_full_name()


class Restaurant(models.Model):

    name = models.CharField(_('Name'), max_length=250)
    description = models.CharField(_('Description'), max_length=250, blank=True)
    country = models.CharField(max_length=100)
    street = models.CharField(_('Street'), max_length=100, blank=True)
    extra_street = models.CharField(_('Extra_street'), max_length=100, blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    state = models.CharField(_('State'), max_length=100, blank=True)
    zip_code = models.CharField(_('Zip code'), max_length=100, blank=True)
    email = models.EmailField(_('Email'), max_length=70, blank=True)
    website = models.CharField(_('Web'), max_length=250, blank=True)
    tax = models.DecimalField(_('Tax'), max_digits=20, decimal_places=6, default=7.000)
    error = models.DecimalField(_('Margin_error'), max_digits=10, decimal_places=6, default=0.001)
    mp_cost = models.DecimalField(_('Mp_cost'), max_digits=10, decimal_places=6, default=25.00)
    manager = models.ForeignKey(get_user_model(), related_name='Restaurant_Manager', on_delete=models.CASCADE, null=True)
    chefs = models.ManyToManyField(get_user_model(), related_name='Restaurant_Chefs')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Restaurant:detail', kwargs={
               'id': self.id
            })


# create a profile user model
class Profile(models.Model):
    # declare profile attributes
    MANAGER = 1
    CHEF = 2
    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (CHEF, 'Chef'),
    )
    user = models.OneToOneField(get_user_model(), related_name='Profile_user', null=True, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)
    restaurant = models.OneToOneField(Restaurant, related_name='Active_Restaurant', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Provider(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(_('Description'), max_length=250, blank=True)
    country = models.CharField(max_length=100)
    street = models.CharField(_('Street'), max_length=100, blank=True)
    extra_street = models.CharField(_('Extra_street'), max_length=100, blank=True)
    city = models.CharField(_('City'), max_length=100, blank=True)
    state = models.CharField(_('State'), max_length=100, blank=True)
    zip_code = models.CharField(_('Zip code'), max_length=100, blank=True)
    contact = models.CharField(_('Contact'), max_length=100, blank=True)
    email = models.EmailField(_('Email'),max_length=70, blank=True, unique=True)
    phone = models.CharField(_('Phone'), max_length=12)
    web = models.CharField(_('Web'), max_length=250, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Provider:detail', kwargs={
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

    name = models.CharField(_('Name'), max_length=250)
    type = models.CharField(_('Type'), max_length=50,choices=CATEGORY_CHOICES, default=GROCERY)
    presentation = models.CharField(_('Presentation'), max_length=50, choices=PRESENTATION_CHOICES, default=GRAM)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(_('Description'), max_length=999)
    price = models.DecimalField(_('Price'), max_digits=20, decimal_places=10)
    qty = models.DecimalField(_('Quantity'), max_digits=20, decimal_places=10)
    error = models.DecimalField(_('Error'), max_digits=10, decimal_places=6, default=0.01)
    provider = models.ForeignKey(Provider, related_name='Ingredient_provider', on_delete=models.CASCADE)
    chef = models.ForeignKey(get_user_model(), related_name='Ingredient_chef', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Ingredient:detail', kwargs={
            'id': self.id
        })


class Receta(models.Model):

    name = models.CharField(_('Name'), max_length=100)
    description = models.CharField(_('Description'), max_length=250, blank=True)
    is_complete = models.BooleanField(_('Is complete'),default=False)
    cost = models.DecimalField(_('Cost'),max_digits=20, decimal_places=10)
    portions = models.DecimalField(_('Portions'),max_digits=20, decimal_places=10, default=1.0)
    mpcost = models.DecimalField(_('Mp_cost'),max_digits=20, decimal_places=10, default=0.0)
    prepacost = models.DecimalField(_('Prep_cost'),max_digits=20, decimal_places=10, default=0.0)
    portioncost = models.DecimalField(_('P_cost'),max_digits=20, decimal_places=10, default=0.0)
    mpestablish = models.DecimalField(_('E_cost'),max_digits=20, decimal_places=10, default=0.0)
    errormargin = models.DecimalField(_('Error_margin'),max_digits=20, decimal_places=10, default=0.01)
    realratemp = models.DecimalField(_('Real_price'),max_digits=20, decimal_places=10, default=0.0)
    saleprice = models.DecimalField(_('Sale_price'),max_digits=20, decimal_places=10, default=0.0)
    menuprice = models.DecimalField(_('Menu_price'),max_digits=20, decimal_places=10, default=0.0)
    realsaleprice = models.DecimalField(_('R_price'),max_digits=20, decimal_places=10, default=0.0)
    taxportion = models.DecimalField(_('Tax'),max_digits=20, decimal_places=10,default=0.0)
    duration = models.DurationField(_('Duration'), default="00:01:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, null=True, on_delete=models.SET_NULL, related_name='Receta_restaurant')
    chef = models.ForeignKey(get_user_model(), related_name='Receta_chef', null=True, on_delete=models.SET_NULL)
    items = models.ManyToManyField(Ingredient, through='Steps', through_fields=('receta', 'ingredient'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Receta:detail', kwargs={
            'id': self.id
        })


class Steps(models.Model):

    qty = models.DecimalField(_('Qty'), max_digits=20,decimal_places=10, default=1.0)
    preparation = models.CharField(_('Preparation'), max_length=250)
    duration = models.DurationField(_('Step_duration'), default="00:01:00")
    error = models.DecimalField(_('Error'), max_digits=10, decimal_places=6,  default=0.001)
    receta = models.ForeignKey(Receta, related_name='steps_receta', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='steps_ingredient', on_delete=models.CASCADE)
    cost_gmu = models.DecimalField(_('Cost_gmu'), max_digits=20, decimal_places=10, default=0.0)
    cost_total = models.DecimalField(_('Cost_total'), max_digits=20, decimal_places=10, default=0.0)
    cost_waste = models.DecimalField(_('Cost_waste'), max_digits=20, decimal_places=10, default=0.0)
    error = models.DecimalField(_('Error'), max_digits=20, decimal_places=10, default=0.01)

    def __str__(self):
        return self.ingredient.name

    def get_absolute_url(self):
        return reverse('Step:detail', kwargs={
            'id': self.id
       })

