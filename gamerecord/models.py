from django.db import models

# Create your models here.

class record(models.Model):

    gamenumber = models.IntegerField()
    user = models.ManyToManyField('Gameuser', related_name='ingameuser')
    


class Gameuser(models.Model):

    userNum = models.IntegerField()
    mmr = models.IntegerField()
    nickname = models.CharField(max_length=90)
    rank = models.IntegerField()
    totalGames = models.IntegerField()
    winrate = models.DecimalField(max_digits=6, decimal_places=1)
    averageKills = models.DecimalField(max_digits=6, decimal_places=2)
    gameId = models.IntegerField()