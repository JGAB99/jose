# Generated by Django 5.1.2 on 2024-11-04 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('math_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='is_correct',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
