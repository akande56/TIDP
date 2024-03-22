# Generated by Django 4.2.11 on 2024-03-22 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0004_alter_schedule_meeting_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule_meeting',
            name='attachment',
            field=models.ImageField(blank=True, null=True, upload_to='meetingfiles/'),
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