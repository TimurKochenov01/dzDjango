from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Employee
from .serializers import EmployeeSerializer
from datetime import date

class IsViewer(permissions.BasePermission):
    """Права смотрителя - может перемещать сотрудников"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Смотритель может менять только номер стола
        return request.method == 'PATCH' and 'desk_number' in request.data

class IsAdmin(permissions.BasePermission):
    """Права администратора - полный доступ"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['skills', 'first_name', 'last_name']
    
    def get_permissions(self):
        """Назначаем права в зависимости от действия"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsViewer | IsAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def filter_by_experience(self, request):
        """Фильтрация по стажу"""
        min_days = request.query_params.get('min_days')
        max_days = request.query_params.get('max_days')
        
        queryset = self.get_queryset()
        
        if min_days:
            min_date = date.today() - timedelta(days=int(min_days))
            queryset = queryset.filter(hire_date__lte=min_date)
        
        if max_days:
            max_date = date.today() - timedelta(days=int(max_days))
            queryset = queryset.filter(hire_date__gte=max_date)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)