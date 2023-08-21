from django.db import models
import datetime
# Create your models here.
from .validators import *

team_list = (
        ('경영팀','경영팀'),
        ('고객대응팀','고객대응팀'),
        ('기술지원팀','기술지원팀'),
        ('전략기획팀','전략기획팀'),
        ('소속없음','소속없음'),
    )


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    create_user = models.CharField(max_length=80)
    team = models.CharField(max_length=80, choices=team_list)
    title = models.CharField(max_length=80, validators=[validate_test])
    content = models.CharField(max_length=80)
    is_complete = models.BooleanField(default=False)
    compleated_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    subchoic = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

class SubTask(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.CharField(null=True, blank=True,max_length=80,choices=team_list)
    is_complete = models.BooleanField(default=False)
    compleated_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    task = models.ForeignKey(Task,null=False,blank=False, related_name='subtasks', on_delete=models.CASCADE)
    