# Generated by Django 4.2.2 on 2023-08-21 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0002_alter_character_atkspeed_alter_character_attack_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='atkspeed',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='character',
            name='attack',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='character',
            name='defense',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='character',
            name='hp',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='character',
            name='hpregen',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='character',
            name='speed',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='character',
            name='stamina',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='character',
            name='stregen',
            field=models.FloatField(),
        ),
    ]
