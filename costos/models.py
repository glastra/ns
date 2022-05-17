import locale
from re import sub
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.db import models
from django.db.models import Model
from django_countries import widgets, countries
from djmoney.models.fields import MoneyField as BaseMoneyField
from django.core.validators import MinValueValidator, MaxValueValidator
from moneyed import Money, USD, COP
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_quill.fields import QuillField
from django.db.models import Count, Sum

percentage_validators = [MinValueValidator(0.01), MaxValueValidator(100)]


def validate_min_percentage(value):
    if value < 0:
        print('cannot be less than 0.001', value)


def validate_max_percentage(value):
    if value > 100:
        print('cannot be more than 100', value)


COUNTRIES = (
    ('COL', _('Colombia')),
    ('US', _('United States'))
)


class MoneyField(BaseMoneyField):
    serialize = True

    @property
    def get_amount(self):
        return self.check(self)



class CountryField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 3)
        kwargs.setdefault('choices', COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"


class User(AbstractUser):

    phone = models.CharField(
        _('phone'),
        max_length=12
    )

    is_verified = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.get_full_name()


class Company(models.Model):
    ANONYMOUS_USER_ID = 1

    name = models.CharField(
        _('name'),
        max_length=250,
    )
    description = models.CharField(
        _('description'),
        max_length=250,
        blank=True,
    )

    owner = models.ForeignKey(
        get_user_model(),
        related_name='companies',
        default=ANONYMOUS_USER_ID,
        on_delete=models.SET_DEFAULT,
        limit_choices_to={'is_verified': True},
    )

    identification = models.CharField(
        _('identification'),
        max_length=20,
        blank=True,
    )

    country = CountryField()

    street = models.CharField(
        _('street'),
        max_length=100,
        blank=True,
    )
    extra_street = models.CharField(
        _('extra street'),
        max_length=100,
        blank=True,
    )
    city = models.CharField(
        _('city'),
        max_length=100,
        blank=True,
    )
    state = models.CharField(
        _('state'),
        max_length=100,
        blank=True,

    )
    zipcode = models.CharField(
        _('zipcode'),
        max_length=100,
        blank=True,
    )
    contact = models.CharField(
        _('contact'),
        max_length=100,
        blank=True,
    )
    phone = models.CharField(
        _('phone'),
        max_length=250,
        blank=True,
    )
    website = models.CharField(
        _('website'),
        max_length=250,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Company:detail', kwargs={
            'id': self.id
        })


class Restaurant(models.Model):

    ANONYMOUS_USER_ID = 1
    ANONYMOUS_COMP_ID = 1

    name = models.CharField(
        _('name'),
        max_length=250,
    )

    description = models.CharField(
        _('Description'),
        max_length=250,
        blank=True,
    )

    company = models.OneToOneField(
        Company,
        related_name='restaurants',
        verbose_name=_('Select Company'),
        default=ANONYMOUS_COMP_ID,
        on_delete=models.SET_DEFAULT,
    )

    manager = models.ForeignKey(
        get_user_model(),
        related_name='restaurants',
        verbose_name=_('Manager'),
        default=ANONYMOUS_USER_ID,
        on_delete=models.SET_DEFAULT,
    )

    identification = models.CharField(
        _('identification'),
        max_length=20,
    )

    chef = models.ManyToManyField(
        get_user_model(),
    )

    tax = models.DecimalField(
        _('tax'),
        max_digits=8,
        decimal_places=2,
        default=7.00,
    )
    decrease = models.FloatField(
        _('decrease'),
        default=0.00,
        validators=[validate_max_percentage]
    )
    raw_cost = models.DecimalField(
        _('material cost'),
        max_digits=5,
        decimal_places=2,
        default=0.25,
    )

    website = models.CharField(
        _('Web'),
        max_length=250,
        blank=True,
    )

    country = CountryField()

    street = models.CharField(
        _('street'),
        max_length=100,
        blank=True,
    )
    extra_street = models.CharField(
        _('extra street'),
        max_length=100,
        blank=True,

    )
    city = models.CharField(
        _('city'),
        max_length=100,
        blank=True,

    )
    state = models.CharField(
        _('State'),
        max_length=100,
        blank=True
    )
    zipcode = models.CharField(
        _('zipcode'),
        max_length=100,
        blank=True
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.id = None

    def __str__(self):
        return f"{self.name},{self.description}"

    def get_absolute_url(self):
        return reverse('Restaurant:detail', kwargs={
               'id': self.id
            })

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Restaurant, self).save()


# create a profile user model
class Profile(models.Model):

    ANONYMOUS_RESTAURANT_ID = 1

    # declare profile attributes
    user = models.OneToOneField(
        get_user_model(),
        related_name='profile',
        null=True,
        on_delete=models.CASCADE,
    )
    OWNER = 1
    MANAGER = 2
    CHEF = 3
    ROLE_CHOICES = (
        (OWNER, 'Owner'),
        (MANAGER, 'Manager'),
        (CHEF, 'Chef'),
    )

    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        default=3
    )
    restaurant = models.OneToOneField(
        Restaurant,
        related_name='profile',
        default=ANONYMOUS_RESTAURANT_ID,
        on_delete=models.SET_DEFAULT,
    )

    country = CountryField()

    # def __str__(self):
    #     return self.user.get_full_name()


class Provider(models.Model):

    name = models.CharField(
        max_length=100,
        verbose_name=_('Provider Name')
    )
    description = models.CharField(
        _('Description'),
        max_length=250,
        blank=True,
    )

    country = CountryField()

    street = models.CharField(
        _('Street'),
        max_length=100,
        blank=True
    )
    extra_street = models.CharField(
        _('ExtraStreet'),
        max_length=100,
        blank=True
    )
    city = models.CharField(
        _('City'),
        max_length=100,
        blank=True
    )
    state = models.CharField(
        _('State'),
        max_length=100,
        blank=True
    )
    zipcode = models.CharField(
        _('zipcode'),
        max_length=100,
        blank=True
    )
    contact = models.CharField(
        _('Contact'),
        max_length=100,
        blank=True
    )
    email = models.EmailField(
        _('Email'),
        max_length=70,
        blank=True,
        unique=True
    )
    phone = models.CharField(
        _('Phone'),
        max_length=12
    )
    web = models.CharField(
        _('Web'),
        max_length=250,
        blank=True
    )

    def get_absolute_url(self):
        return reverse('provider_detail', kwargs={
            'pk': self.pk
            })

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    ANONYMOUS_USER_ID = 1
    GRAM = "gram"
    UNIT = "unit"
    LITER = "liter"
    MILLILITER = "milliliter"
    KILOGRAM = "kilogram"
    OZ = "onz"
    POUND = "pound"

    PRESENTATION_CHOICES = [
        (GRAM, "Gram"),
        (POUND, "Pound"),
        (LITER, "Liter"),
        (UNIT, "Unit"),
        (MILLILITER, "Milliliter"),
        (KILOGRAM, "Kilogram"),
        (OZ, "Onz")
    ]

    GROCERY = "grocery"
    PROTEIN = "protein"
    FRUVER = "fruVer"
    CATEGORY_CHOICES = [
        (GROCERY, "Grocery"),
        (PROTEIN, "Protein"),
        (FRUVER, "FruVer")
    ]
    chef = models.ForeignKey(
        get_user_model(),
        related_name='ingredients',
        default=ANONYMOUS_USER_ID,
        on_delete=models.SET_DEFAULT,
        limit_choices_to={'is_verified': True},
    )
    provider = models.ForeignKey(
        Provider,
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        _('name'),
        max_length=250,
    )
    description = models.TextField(
        _('description'),
        max_length=999,

    )
    type = models.CharField(
        _('type'),
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=GROCERY,
    )
    presentation = models.CharField(
        _('presentation'),
        max_length=50,
        choices=PRESENTATION_CHOICES,
        default=GRAM,
    )

    realQty = models.DecimalField(
        _('realqty'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
    )

    qty1 = models.DecimalField(
        _('quantity1'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
    )
    qty2 = models.DecimalField(
        _('quantity2'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
    )
    qtyTotal = models.DecimalField(
        _('totalqty'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
    )
    qtyUsed = models.DecimalField(
        _('totalUsed'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
    )
    qtyPend = models.DecimalField(
        _('totalPend'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
    )
    price = MoneyField(
        _('price'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
    )

    cost = MoneyField(
        _('cost'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.0,
    )

    decrease = models.FloatField(
        _('decrease'),
        default=0.1,
        validators=[validate_max_percentage]
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now_add=True,
    )

    is_track = models.BooleanField(
        default=False,
    )
    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.qty2 = self.get_decrease_qty
        if self.decrease == 0:
            print(self.qty2)
            self.decrease = self.get_decrease_percent
        self.cost = self.cost_gmu
        super(Ingredient, self).save()

    def get_absolute_url(self):
        return reverse('ingredient_detail', kwargs={
            'pk': self.pk
        })


    @property
    def get_decrease_qty(self):
        return float(self.qty1) - (float(self.qty1) * self.decrease)

    @property
    def get_decrease_percent(self):
        return 100 * abs(self.qty2 - self.qty1) / self.qty1

    @property
    def get_efficiency(self):
        return abs(100-self.decrease)

    @property
    def cost_gmu(self):
        self.realQty = self.qty1
        if self.presentation == self.LITER:
            self.realQty = self.qty1 * 1000
        if self.presentation == self.KILOGRAM:
            self.realQty = self.qty1 * 1000
        if self.presentation == self.POUND:
            self.realQty = self.qty1 * 500

        gmu_cost = self.price / self.realQty

        return gmu_cost


class RecipeManager(models.Manager):
    def create_recipe(self, name):
        recipe = self.create(name=name)
        # do something with the recipe
        return recipe


class CompleteRecipe(models.Manager):
    def get_queryset(self):
        return super(CompleteRecipe, self).get_queryset().filter(is_copmlete=True)


class Recipe(models.Model):

    ANONYMOUS_USER_ID = 1
    ANONYMOUS_RESTAURANT_ID = 1

    chef = models.ForeignKey(
        get_user_model(),
        related_name='recipes',
        default=ANONYMOUS_USER_ID,
        on_delete=models.SET_DEFAULT,
    )

    restaurant = models.ForeignKey(
        Restaurant,
        default=ANONYMOUS_RESTAURANT_ID,
        on_delete=models.SET_DEFAULT,
        related_name='recipes',
    )

    name = models.CharField(
        _('name'),
        max_length=100,
    )

    description = QuillField(
        blank=True
    )

    cost = MoneyField(
        _('cost'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )

    portions = models.DecimalField(
        _('portions'),
        max_digits=18,
        decimal_places=6,
        default=1.0,

    )
    raw_material_cost = MoneyField(
        _('raw_material_cost'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )

    prep_cost = MoneyField(
        _('prep_cost'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )
    portion_cost = MoneyField(
        _('portion_cost'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )
    establish_raw_material_cost = MoneyField(
        _('establish_raw_material_cost'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )
    margin_error = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=0.1,
        validators=[MinValueValidator(000.001),
                    MaxValueValidator(100)]

    )
    real_price = MoneyField(
        _('real_price'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )
    sales_price = MoneyField(
        _('sales_price'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )
    menu_price = MoneyField(
        _('menu_price'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=1.00,
    )
    real_sales_price = MoneyField(
        _('real_sales_price'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )
    tax_portion = MoneyField(
        _('tax_portion'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.00,
    )
    duration = models.DurationField(
        _('duration'),
        default="00:01:00",
    )
    items = models.ManyToManyField(
        Ingredient,
        through='step',
        through_fields=('recipe', 'ingredient')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_complete = models.BooleanField(
        _('Is complete'),
        default=False,
    )

    is_track = models.BooleanField(
        default=False,
    )

    objects = models.Manager()  # The default manager.

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            super(Recipe, self).save(*args, **kwargs)
        super(Recipe, self).save(*args, **kwargs)

        super(Recipe, self).save()

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={
            'pk': self.pk
        })

    @classmethod
    def create(cls, name, items):
        recipe = cls(name=name, items=items)
        # do something with the recipe
        return recipe

    @property
    def cal_cost(self):
        s = self.items
        result = s.aggregate(sum=Sum('cost'))['sum']
    #    return f"${result:,.2f}"
        return result

    @property
    def cal_portion_cost(self):
        s = self.items
        result = s.aggregate(sum=Sum('cost'))['sum']
        result = float(result / self.portions)
        #return f"${result:,.2f}"
        return result

    @property
    def cal_error(self):
        s = self.items
        result = s.aggregate(sum=Sum('cost'))['sum']
        print(result)
        print(self.cal_portion_cost)
        temp = float(self.margin_error / 100)
        result = float(result) * temp
        #return f"${result:,.2f}"
        return result

    @property
    def cal_prep_cost(self):
        s = self.items
        result = s.aggregate(sum=Sum('cost'))['sum']
        error = float(result * (self.margin_error / 100))
        final = float(result) + float(error)
        #return f"${final:,.2f}"
        return final


    @property
    def cal_pot_price(self):
        s = self.items
        result = s.aggregate(sum=Sum('cost'))['sum']
        error = float(result * (self.margin_error / 100))
        final = float(result) + float(error)
        #return f"${final:,.2f}"
        return final


    @property
    def cal_tax(self):
        s = self.items
        result = s.aggregate(sum=Sum('cost'))['sum']
        error = float(result * (self.margin_error / 100))
        final = float(result) + float(error)
        tax = final * float(7/100)
        #return f"${final:,.2f}"
        return tax


    @property
    def cal_sale_price(self):
        s = self.items
        result = s.aggregate(sum=Sum('cost'))['sum']
        error = float(result * (self.margin_error / 100))
        final = float(result) + float(error)
        tax = final * float(7 / 100)
        final = tax + final
        # return f"${final:,.2f}"
        return final


class Step(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='steps',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='steps',
        on_delete=models.CASCADE,
    )
    qty1 = models.DecimalField(
        _('qty1'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
    )
    qty2 = models.DecimalField(
        _('qty2'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
    )
    preparation = QuillField(
        blank=True
    )

    duration = models.DurationField(
        _('duration'),
        default="00:01:00"
    )
    decrease = models.DecimalField(
        _('decrease'),
        max_digits=18,
        decimal_places=6,
        default=1.0,
        validators=[MinValueValidator(0.01),
                    MaxValueValidator(100.000)]
    )
    cost_gmu = MoneyField(
        _('cost_gmu'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.000,

    )
    cost_total = MoneyField(
        _('cost_total'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.000,
    )
    cost_waste = MoneyField(
        _('cost_waste'),
        max_digits=18,
        decimal_places=6,
        default_currency='COP',
        default=0.000,
    )

    def __str__(self):
        return self.recipe.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.cost_total = self.calculate_cost
        # locale.setlocale(locale.LC_ALL, '')
        # conv = locale.localeconv()

       #  amount = self.cost_total.get_amount
       #
       # # amount = float(self.cost_total)
       #  print(amount)
       #  self.cost_gmu = float(amount / self.qty1)
       #  self.cost_waste = amount * self.decrease
        print(self.cost_gmu)
        super(Step, self).save()

    def get_absolute_url(self):
        return reverse('recipe_steps_update', kwargs={
            'pk': self.pk
            })

    @property
    def calculate_cost(self):
        ing = self.ingredient
        result = self.qty1 * ing.cost
        #return f"${result:,.2f}"
        return result


