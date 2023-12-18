# Generated by Django 3.2 on 2023-12-17 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_contractors_company_name'),
        ('procurement', '0016_alter_precurement_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='precurement',
            name='contractor',
        ),
        migrations.AddField(
            model_name='precurement',
            name='contractor',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='project_contractors', to='accounts.Contractors'),
        ),
    ]
