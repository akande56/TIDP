# Generated by Django 3.2 on 2023-07-29 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_contractors_documents'),
        ('procurement', '0012_precurement_precurement_contractors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='precurement',
            name='contractor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_contractors', to='accounts.contractors'),
        ),
    ]