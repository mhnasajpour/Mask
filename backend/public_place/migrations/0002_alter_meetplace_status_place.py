# Generated by Django 4.1 on 2022-08-12 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_place', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetplace',
            name='status_place',
            field=models.CharField(choices=[('W', 'White'), ('R', 'Red')], max_length=1),
        ),
    ]
