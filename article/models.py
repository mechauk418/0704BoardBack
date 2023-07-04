from django.db import models
from django.conf import settings
# Create your models here.

subject_list = [
        ('일반','일반'),
        ('정보','정보'),
        ('사진','사진'),
        ('공략','공략'),
        ('자랑','자랑'),
]

class Article(models.Model):

    title = models.CharField(max_length=80)
    content = models.TextField()
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hits = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    subject = models.CharField(max_length=50, choices=subject_list)
    


    def __str__(self):
        return self.title
    
