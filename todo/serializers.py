from rest_framework import serializers, fields
from .models import *

class SubTaskSerializer(serializers.ModelSerializer):

    task = serializers.ReadOnlyField(source="task.id")
    
    class Meta:
        model = SubTask
        fields = [
            'id',
            'team',
            'is_complete',
            'compleated_date',
            'task'
        ]


team_list = (
        ('경영팀','경영팀'),
        ('고객대응팀','고객대응팀'),
        ('기술지원팀','기술지원팀'),
        ('전략기획팀','전략기획팀'),
        ('소속없음','소속없음'),
    )

class TaskSerializer(serializers.ModelSerializer):
    team = serializers.ChoiceField(choices = team_list, style={'base_template' : 'radio.html'})
    test = serializers.SerializerMethodField()
    subchoic = serializers.MultipleChoiceField(choices = team_list, write_only=True)
    
    def get_test(self,obj):
        tes = obj.subtasks.all()
        return SubTaskSerializer(instance=tes, many=True, context = self.context).data

    # def validate(self, attrs):
    #     if 'error' not in attrs['title']:
    #         raise ValidationError('error')
    #     return super().validate(attrs)

    class Meta:
        model = Task
        fields = [
            'id',
            'create_user',
            'team',
            'title',
            'content',
            'is_complete',
            'compleated_date',
            'test',
            'subchoic',
        ]
        read_only_fields = ['is_complete', 'create_user']
        

    def create(self, validated_data):
        instance = Task.objects.create(**validated_data)
        ch_list = self.context['request'].data.getlist('subchoic')
        for team in ch_list:
            print(team)
            SubTask.objects.create(team=team, task =instance)

        return instance