from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Employee

def home(request):
    total_employees = Employee.objects.count()
    
    latest_employees = Employee.objects.order_by('-hire_date')[:4]
    
    context = {
        'total_employees': total_employees,
        'latest_employees': latest_employees,
    }
    return render(request, 'main/home.html', context)

def employee_list(request):
    employees_list = Employee.objects.all().order_by('-hire_date')
    paginator = Paginator(employees_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main/employee_list.html', context)

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    all_images = employee.gallery.all()
    first_image = all_images.first() if all_images.exists() else None
    other_images = all_images[1:] if all_images.count() > 1 else []
    
    context = {
        'employee': employee,
        'first_image': first_image,
        'other_images': other_images,
    }
    return render(request, 'main/employee_detail.html', context)