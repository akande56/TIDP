# Generated by Django 3.2 on 2024-02-18 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondance', '0004_alter_routing_sender_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routing',
            name='sender_stage',
            field=models.CharField(choices=[('Clearing', 'Clearing'), ('Done', 'Done')], default='Done', max_length=200),
        ),
    ]