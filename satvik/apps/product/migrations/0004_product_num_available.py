# Generated by Django 3.1.7 on 2021-04-10 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_available',
            field=models.IntegerField(default=1),
        ),
    ]