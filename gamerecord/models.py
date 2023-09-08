from django.db import models

# Create your models here.



class Gameuser(models.Model):

    userNum = models.IntegerField()
    mmr = models.IntegerField()
    nickname = models.CharField(max_length=90)
    rank = models.IntegerField()
    totalGames = models.IntegerField()
    winrate = models.DecimalField(max_digits=6, decimal_places=1)
    averageKills = models.DecimalField(max_digits=6, decimal_places=2)
    updatedate = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.nickname




class Record(models.Model):

    gamenumber = models.IntegerField()
    user = models.ForeignKey(Gameuser,on_delete=models.CASCADE)
    character = models.IntegerField()
    beforemmr = models.IntegerField()
    aftermmr = models.IntegerField()
    gamerank = models.IntegerField()
    playerkill = models.IntegerField()
    playerAss = models.IntegerField()
    mosterkill = models.IntegerField()
    startDtm = models.DateTimeField()
    mmrGain = models.IntegerField()


    
