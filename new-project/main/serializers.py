from rest_framework import serializers
from .models import Employee, EmployeeImage

class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = ['id', 'image', 'order']

class EmployeeSerializer(serializers.ModelSerializer):
    gallery = EmployeeImageSerializer(many=True, read_only=True)
    work_experience_days = serializers.ReadOnlyField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 
            'gender', 'skills', 'skill_levels', 'description',
            'hire_date', 'desk_number', 'gallery', 'work_experience_days'
        ]