# Generated by Django 3.2 on 2023-12-24 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_contractors_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractordocument',
            name='file',
            field=models.ImageField(upload_to='contractor_docs/'),
        ),
    ]