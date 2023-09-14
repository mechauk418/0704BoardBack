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
    gamerank = models.IntegerField() # 게임 등수
    playerkill = models.IntegerField() # 킬
    playerAss = models.IntegerField() # 어시
    mosterkill = models.IntegerField() # 동물킬
    startDtm = models.DateTimeField() # 게임 시작 시간
    mmrGain = models.IntegerField() # mmr 획득량
    damageToPlayer = models.IntegerField(blank=True, default=0) # 플레이어 피해량
    damageToMonster = models.IntegerField(blank=True, default=0) # 동물 피해량
    premaid = models.IntegerField(blank=True, default=0) # 사전 구성팀
    useWard = models.IntegerField(blank=True, default=0) # 카메라 사용 갯수
    useConsole = models.IntegerField(blank=True, default=0) # 콘솔 작동 횟수
    


# skillOrderInfo = 스킬 레벨업 순서

# escapeState = 1이면 탈출 실패, 2이면 전투 패배, 3이면 탈출

# tacticalSkillGroup = 최종 전술 스킬 종류

# tacticalSkillLevel = 최종 전술 스킬 레벨