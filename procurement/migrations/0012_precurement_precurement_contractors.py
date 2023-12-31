# Generated by Django 3.2 on 2023-07-28 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0009_remove_contractors_documents'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('procurement', '0011_auto_20230728_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Precurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='contract title', max_length=20)),
                ('category', models.CharField(choices=[('open tender', 'open tender'), ('selective tender', 'selective tender'), ('internal labour', 'internal labour')], help_text='broadcast range', max_length=20)),
                ('responsibilty', models.CharField(max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('tender_type', models.CharField(choices=[('open tender', 'open tender'), ('selective tender', 'selective tender'), ('internal labour', 'internal labour')], help_text='audience', max_length=20)),
                ('description', models.CharField(default='details of project', max_length=30)),
                ('budget', models.CharField(max_length=20)),
                ('priority', models.CharField(choices=[('HIGHEST', 'HIGHEST'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW'), ('LOWEST', 'LOWEST')], default=3, max_length=20)),
                ('contractor', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_contractors', to='accounts.contractors')),
            ],
        ),
        migrations.CreateModel(
            name='Precurement_contractors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited', to=settings.AUTH_USER_MODEL)),
                ('precurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertisedPrecurement', to='procurement.precurement')),
            ],
            options={
                'verbose_name': 'Precurement_contractors',
                'verbose_name_plural': 'Precurement_contractors',
            },
        ),
    ]
