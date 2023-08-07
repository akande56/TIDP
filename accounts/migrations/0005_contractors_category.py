# Generated by Django 3.2 on 2023-07-13 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_contractors_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractors',
            name='category',
            field=models.CharField(choices=[(1, 'Software'), (2, 'Telecommunication'), (3, 'Construction'), (4, 'others')], default='Software', max_length=50),
        ),
    ]
