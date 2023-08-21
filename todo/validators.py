from django.core.exceptions import ValidationError

def validate_test(value):
    if 'k' in value:
        raise ValidationError('유효성 검사 실패')