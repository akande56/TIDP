# Generated by Django 3.2 on 2023-07-28 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_contractors_documents'),
        ('procurement', '0009_alter_precurement_contractor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='precurement',
            name='contractor',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_contractors', to='accounts.contractors'),
        ),
    ]
