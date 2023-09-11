from django.db import models

# Create your models here.


class Character(models.Model):

    name = models.CharField(max_length=80)

    attack = models.DecimalField(max_digits=6, decimal_places=3)
    hp = models.DecimalField(max_digits=6, decimal_places=3)
    hpregen = models.DecimalField(max_digits=6, decimal_places=3)
    stamina = models.DecimalField(max_digits=6, decimal_places=3)
    stregen = models.DecimalField(max_digits=6, decimal_places=3)
    defense = models.DecimalField(max_digits=6, decimal_places=3)
    atkspeed = models.DecimalField(max_digits=6, decimal_places=3)
    speed = models.DecimalField(max_digits=6, decimal_places=3)
    koreanname = models.CharField(max_length=80, blank=True)

# s = Character.objects.create(name='AbiGail', attack = 30, hp = 800, hpregen = 1.5, stamina = 500, defense = 30, atkspeed=1.5, speed=3.5, stregen = 1.5)