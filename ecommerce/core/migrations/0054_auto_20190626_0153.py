# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-26 01:53


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_user_lms_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='enable_microfrontend_for_basket_page',
            field=models.BooleanField(
                default=False,
                help_text='Use the microfrontend implementation of the basket page instead of the server-side template',
                verbose_name='Enable Microfrontend for Basket Page'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='payment_microfrontend_url',
            field=models.URLField(
                blank=True,
                help_text='URL for the Payment Microfrontend (used if Enable Microfrontend for Basket Page is set)',
                null=True, verbose_name='Payment Microfrontend URL'),
        ),
    ]
