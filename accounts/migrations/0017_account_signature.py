# Generated by Django 3.2 on 2024-02-25 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_userpersona_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='signature',
            field=models.ImageField(blank=True, null=True, upload_to='signatures/'),
        ),
    ]