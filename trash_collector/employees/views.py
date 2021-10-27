from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.apps import apps
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
import datetime
from customers.models import Customer

from .models import Employee

# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.
Customer = apps.get_model('customers.Customer')

@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        today = date.today()
        logged_in_employee_zip_code = logged_in_employee.zip_code
        customers_in_zip_code = Customer.objects.filter(zip_code=logged_in_employee_zip_code)
        pickups_today = Customer.objects.filter(pickups_today=today.strftime("%A"))
        non_sus_accounts = pickups_today.exclude(suspend_start__lt=today, suspend_end__gt=today)
        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'customers_in_zip_code' : customers_in_zip_code,
            'pickups_today' : pickups_today,
            'non_sus_accounts' : non_sus_accounts
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))


# def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db for Customers
    # Customer = apps.get_model('customers.Customer')
    # return render(request, 'employees/index.html')

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user, address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')

@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employees': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)

@login_required
def confirm_pickup_charge_balance(customer_id):
    customer_charge = Customer.objects.get(id=customer_id)
    customer_charge.balance += 20
    customer_charge.save()
    return HttpResponseRedirect(reverse('employees:index'))