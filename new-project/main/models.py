from django.db import models
from django.contrib.auth.models import User  # ← ДОБАВЬТЕ ЭТОТ ИМПОРТ
from django.utils import timezone
from datetime import date

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Отчество')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    skills = models.TextField(verbose_name='Навыки', help_text='Перечислите навыки через запятую')
    skill_levels = models.TextField(verbose_name='Уровни навыков', help_text='Уровни через запятую (1-10)')
    description = models.TextField(verbose_name='Описание', blank=True)
    hire_date = models.DateField(default=timezone.now, verbose_name='Дата приёма на работу')
    desk_number = models.IntegerField(default=1, verbose_name='Номер стола')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['-hire_date']

    def __str__(self):
        name = f"{self.last_name} {self.first_name}"
        if self.middle_name:
            name += f" {self.middle_name}"
        return name

    def get_skills_with_levels(self):
        """Возвращает список навыков с уровнями"""
        skills_list = [skill.strip() for skill in self.skills.split(',') if skill.strip()]
        levels_list = [level.strip() for level in self.skill_levels.split(',') if level.strip()]
        
        result = []
        for i, skill in enumerate(skills_list):
            level = levels_list[i] if i < len(levels_list) else "1"
            result.append(f"{skill} (уровень {level})")
        return result

    def get_work_experience_days(self):
        """Стаж работы в днях"""
        return (date.today() - self.hire_date).days

    def get_first_image(self):
        """Первое изображение из галереи"""
        if self.gallery.exists():
            return self.gallery.first()
        return None

class EmployeeImage(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='employee_images/', verbose_name='Изображение')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Изображение сотрудника'
        verbose_name_plural = 'Изображения сотрудников'
        ordering = ['order']

    def __str__(self):
        return f"Фото {self.employee}"

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('visitor', 'Посетитель'),
        ('viewer', 'Смотритель'),
        ('admin', 'Администратор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='visitor')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"