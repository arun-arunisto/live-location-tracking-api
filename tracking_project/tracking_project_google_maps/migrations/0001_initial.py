# Generated by Django 5.0.6 on 2024-06-25 05:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DestinationTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('address', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('position', models.CharField(max_length=100)),
                ('mail_id', models.EmailField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(null=True)),
                ('starting_point', models.CharField(blank=True, max_length=255, null=True)),
                ('travel_status', models.CharField(choices=[('Stopped', 'Stopped'), ('Traveling', 'Traveling'), ('Reached', 'Reached')], max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Completed', 'Completed')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracking_project_google_maps.employeetable')),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracking_project_google_maps.destinationtable')),
            ],
        ),
        migrations.CreateModel(
            name='LocationTrackingTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('destination_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracking_project_google_maps.destinationtable')),
                ('employee_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracking_project_google_maps.employeetable')),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracking_project_google_maps.tasktable')),
            ],
        ),
    ]
