# Generated by Django 4.2.2 on 2023-09-11 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0004_alter_character_atkspeed_alter_character_attack_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='koreanname',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
