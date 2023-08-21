# Generated by Django 4.2.2 on 2023-08-21 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0003_alter_character_atkspeed_alter_character_attack_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='atkspeed',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='character',
            name='attack',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='character',
            name='defense',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='character',
            name='hp',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='character',
            name='hpregen',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='character',
            name='speed',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='character',
            name='stamina',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
        migrations.AlterField(
            model_name='character',
            name='stregen',
            field=models.DecimalField(decimal_places=3, max_digits=6),
        ),
    ]
