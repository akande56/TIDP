# Generated by Django 3.2 on 2023-12-17 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20230806_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractors',
            name='company_name',
            field=models.CharField(default='default: company name', max_length=60),
        ),
    ]
