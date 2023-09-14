# Generated by Django 3.2 on 2023-07-26 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_contractors_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractors',
            name='business_profile',
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_pic_url',
            field=models.CharField(default=0, max_length=500, null=True),
        ),
    ]