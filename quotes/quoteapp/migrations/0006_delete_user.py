# Generated by Django 5.0.2 on 2024-02-19 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0005_alter_quote_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
