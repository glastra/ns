# Generated by Django 4.0 on 2022-01-31 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('costos', '0002_company_provider_restaurant_company_restaurants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('type', models.CharField(choices=[('grocery', 'Grocery'), ('protein', 'Protein'), ('fruVer', 'FruVer')], default='grocery', max_length=50, verbose_name='type')),
                ('presentation', models.CharField(choices=[('gram', 'Gram'), ('unit', 'Unit'), ('milliliter', 'Milliliter'), ('kilogram', 'Kilogram')], default='gram', max_length=50, verbose_name='presentation')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(max_length=999, verbose_name='description')),
                ('price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('qty', models.DecimalField(decimal_places=10, max_digits=20)),
                ('merma', models.DecimalField(decimal_places=6, default=0.1, max_digits=10)),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_chef', to='auth.user')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_provider', to='costos.provider')),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.CharField(blank=True, max_length=250, verbose_name='description')),
                ('isComplete', models.BooleanField(default=False)),
                ('cost', models.DecimalField(decimal_places=10, max_digits=20)),
                ('portions', models.DecimalField(decimal_places=10, default=1.0, max_digits=20)),
                ('mpcost', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('prepacost', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('portioncost', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('mpestablish', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('errormargin', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('realratemp', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('saleprice', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('menuprice', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('realsaleprice', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('taxportion', models.DecimalField(blank=True, decimal_places=10, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chef', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receta_chef', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Steps',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.DecimalField(decimal_places=10, max_digits=20)),
                ('preparacion', models.CharField(max_length=250)),
                ('merma', models.DecimalField(decimal_places=6, max_digits=10)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps_ingredient', to='costos.ingredient')),
                ('receta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps_receta', to='costos.receta')),
            ],
        ),
        migrations.AddField(
            model_name='receta',
            name='items',
            field=models.ManyToManyField(through='costos.Steps', to='costos.Ingredient'),
        ),
        migrations.AddField(
            model_name='receta',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='costos.restaurant'),
        ),
    ]