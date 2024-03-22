# Generated by Django 4.2.11 on 2024-03-22 15:37

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0017_account_signature'),
        ('meeting', '0002_remove_onlinemeeting_meeting_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule_Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('start_on', models.DateField(blank=True, null=True)),
                ('end_on', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('venue', models.CharField(blank=True, choices=[('online', 'Online'), ('physical', 'Physical')], max_length=1000, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('draft', models.BooleanField(default=False)),
                ('minutes_of_meeting', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('done', models.BooleanField(default=False)),
                ('attachment', models.ImageField(blank=True, null=True, upload_to='meetingfiles/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('link', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(choices=[('up_comming', 'up_comming'), ('previous', 'previous'), ('all', 'all')], default='all', max_length=100)),
                ('paticipants', models.ManyToManyField(related_name='paticipant', to='accounts.account')),
                ('scheduled_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
        migrations.CreateModel(
            name='OnlineMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api', models.CharField(max_length=100)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meeting.schedule_meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agenda', models.CharField(max_length=500)),
                ('minutes', models.IntegerField(blank=True, null=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agendas', to='meeting.schedule_meeting')),
            ],
        ),
    ]
