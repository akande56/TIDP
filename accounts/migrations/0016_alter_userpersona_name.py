# Generated by Django 3.2 on 2024-02-21 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_userpersona_persona_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpersona',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]