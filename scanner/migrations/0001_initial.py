# Generated by Django 5.1.2 on 2024-10-21 06:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScanResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('ip_address', models.CharField(blank=True, max_length=50, null=True)),
                ('grade', models.CharField(max_length=2)),
                ('headers', models.TextField()),
                ('scan_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
