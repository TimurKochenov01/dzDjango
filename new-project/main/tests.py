from django.test import TestCase, Client
from django.urls import reverse
from .models import Employee
from datetime import date

class SimpleTests(TestCase):
    
    def setUp(self):
        """Создаем тестовых сотрудников"""
        self.client = Client()
        
        # Сотрудник 1
        self.emp1 = Employee.objects.create(
            first_name="Иван",
            last_name="Петров",
            gender="M",
            skills="фронтенд, бэкенд",
            skill_levels="8, 9",
            hire_date=date(2024, 1, 15),
            desk_number=1
        )
        
        # Сотрудник 2
        self.emp2 = Employee.objects.create(
            first_name="Мария", 
            last_name="Иванова",
            gender="F",
            skills="тестирование",
            skill_levels="9",
            hire_date=date(2024, 2, 1),
            desk_number=3
        )
    
    # ТЕСТ 1: Проверка адресов
    def test_urls_work(self):
        """Проверяем что страницы открываются"""
        
        # Главная страница
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Список сотрудников
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, 200)
        
        # Карточка сотрудника
        response = self.client.get(f'/employee/{self.emp1.id}/')
        self.assertEqual(response.status_code, 200)
    
    # ТЕСТ 2: Проверка контекста главной страницы
    def test_home_context(self):
        """Проверяем данные на главной странице"""
        response = self.client.get('/')
        
        # Должны быть оба сотрудника
        self.assertEqual(response.context['total_employees'], 2)
        
        # Должны быть 2 последних сотрудника
        latest = response.context['latest_employees']
        self.assertEqual(len(latest), 2)
    
    # ТЕСТ 3: Проверка контекста списка сотрудников
    def test_list_context(self):
        """Проверяем данные в списке сотрудников"""
        response = self.client.get('/employees/')
        
        # Должны быть оба сотрудника
        employees = response.context['page_obj']
        self.assertEqual(len(employees), 2)
    
    # ТЕСТ 4: Проверка контекста карточки сотрудника
    def test_detail_context(self):
        """Проверяем данные в карточке сотрудника"""
        response = self.client.get(f'/employee/{self.emp1.id}/')
        
        # Должны видеть правильного сотрудника
        self.assertEqual(response.context['employee'].first_name, "Иван")
        self.assertEqual(response.context['employee'].last_name, "Петров")
    
    # ТЕСТ 5: Проверка валидатора столов
    def test_desk_validator(self):
        """Проверяем что разработчики и тестировщики не могут сидеть рядом"""
        
        # Создаем разработчика за столом 2
        dev = Employee(
            first_name="Разработчик",
            last_name="Тест",
            gender="M",
            skills="фронтенд",
            skill_levels="8",
            hire_date=date.today(),
            desk_number=2  # Рядом с тестировщиком (стол 3)
        )
        
        # Должна быть ошибка
        from django.core.exceptions import ValidationError
        try:
            dev.full_clean()
            self.fail("Должна быть ошибка валидации!")
        except ValidationError:
            # Ошибка есть - все правильно
            pass
    
    # ТЕСТ 6: Проверка безопасного расположения
    def test_safe_desk(self):
        """Проверяем что можно сидеть на безопасном расстоянии"""
        
        # Создаем разработчика за столом 5 (не рядом)
        dev = Employee(
            first_name="Разработчик",
            last_name="Безопасный", 
            gender="M",
            skills="бэкенд",
            skill_levels="8",
            hire_date=date.today(),
            desk_number=5  # Не рядом с тестировщиком
        )
        
        # Не должно быть ошибки
        try:
            dev.full_clean()
            # Нет ошибки - отлично
        except ValidationError:
            self.fail("Не должно быть ошибки при безопасном расположении!")
    
    # ТЕСТ 7: Проверка методов модели
    def test_model_methods(self):
        """Проверяем методы сотрудника"""
        
        # Проверяем расчет стажа
        days = self.emp1.get_work_experience_days()
        self.assertGreater(days, 0)
        
        # Проверяем навыки с уровнями
        skills = self.emp1.get_skills_with_levels()
        self.assertEqual(len(skills), 2)
    
    # ТЕСТ 8: Проверка несуществующей страницы
    def test_wrong_id(self):
        """Проверяем обработку неправильного ID"""
        response = self.client.get('/employee/999/')
        self.assertEqual(response.status_code, 404)
