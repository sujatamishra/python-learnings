# Generated by Django 3.1.3 on 2020-11-18 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20201114_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
