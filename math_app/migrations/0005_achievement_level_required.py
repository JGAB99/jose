# Generated by Django 5.1.2 on 2024-11-04 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('math_app', '0004_exercise_explanation'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='level_required',
            field=models.IntegerField(default=0),
        ),
    ]