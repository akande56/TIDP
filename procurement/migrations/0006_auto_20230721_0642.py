# Generated by Django 3.2 on 2023-07-21 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('procurement', '0005_alter_precurement_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='precurement',
            name='category',
            field=models.CharField(choices=[('open tender', 'open tender'), ('selective tender', 'selective tender'), ('internal labour', 'internal labour')], help_text='broadcast range', max_length=20),
        ),
        migrations.AlterField(
            model_name='precurement',
            name='tender_type',
            field=models.CharField(choices=[('open tender', 'open tender'), ('selective tender', 'selective tender'), ('internal labour', 'internal labour')], help_text='audience', max_length=20),
        ),
    ]