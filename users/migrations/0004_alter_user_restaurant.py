# Generated by Django 4.1.3 on 2022-11-20 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
        ('users', '0003_alter_user_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant'),
        ),
    ]
