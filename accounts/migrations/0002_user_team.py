# Generated by Django 4.2.2 on 2023-08-16 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.CharField(choices=[('경영팀', '경영팀'), ('고객대응팀', '고객대응팀'), ('기술지원팀', '기술지원팀'), ('전략기획팀', '전략기획팀'), ('소속없음', '소속없음')], default='소속없음', max_length=80),
        ),
    ]
