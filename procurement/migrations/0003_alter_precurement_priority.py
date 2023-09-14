# Generated by Django 3.2 on 2023-07-13 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0002_alter_precurement_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='precurement',
            name='priority',
            field=models.IntegerField(choices=[('1', 'HIGHEST'), ('2', 'MEDIUM'), ('3', 'LOW'), ('4', 'LOWEST')], default=3),
        ),
    ]