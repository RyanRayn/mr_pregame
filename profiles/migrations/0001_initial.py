# Generated by Django 3.1.5 on 2021-05-25 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_type', models.CharField(choices=[('Free', 'Free'), ('Paid', 'Paid')], default='Free', max_length=30)),
                ('price', models.IntegerField(default=30)),
                ('stripe_plan_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=False)),
                ('stripe_customer_id', models.CharField(max_length=40)),
                ('stripe_subscription_id', models.CharField(blank=True, max_length=40)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('postcode', models.CharField(blank=True, max_length=20)),
                ('town_or_city', models.CharField(blank=True, max_length=40)),
                ('street_address1', models.CharField(blank=True, max_length=80)),
                ('street_address2', models.CharField(blank=True, max_length=80)),
                ('membership_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.membership')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
