# Generated by Django 3.2 on 2024-03-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0021_contractoraward'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractoraward',
            name='document',
            field=models.ImageField(blank=True, null=True, upload_to='awarding_documents/'),
        ),
    ]
