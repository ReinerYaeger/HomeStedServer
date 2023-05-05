
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
import datetime
import os

from homested.apartment_scripts.websracper import *


from homested.database_manager import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_user_ip(requests):
    user_ip = requests.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip:
        ip = user_ip.split(',')[0]
    else:
        ip = requests.META.get('REMOTE_ADDR')
    return ip


@login_required(redirect_field_name=None, login_url='login/')
def index(requests):
    return render(requests, 'homested/index.html')


@login_required(redirect_field_name=None, login_url='login/')
def apartment(requests, choice=None):

    number_of_tenants = get_number_of_tenants()

    if requests.method == 'POST':
        if 'insert' in requests.POST:
            form_data = {
                'tenant_name': requests.POST.get('in_tenant_name').strip(),
                'tenant_phone_number': requests.POST.get('in_tenant_phone_number').strip(),
                'arrival_date': requests.POST.get('in_tenant_arrival_date').strip(),
                'departure_date': requests.POST.get('in_tenant_departure_date').strip(),
                'long_term': requests.POST.get('in_tenant_long_term') == 'on',
                'notes': requests.POST.get('in_tenant_notes').strip(),
                'room_location': requests.POST.get('in_room_location').strip(),
                'rent_due_date': requests.POST.get('in_rent_due_date').strip(),
                'rent_amount': requests.POST.get('in_rent_amount').strip(),
                'amount_paid': requests.POST.get('amount_paid').strip(),
                'payment_method': requests.POST.get('in_payment_method').strip(),
                'payment_month_paidfor': requests.POST.get('in_payment_month_paidfor').strip(),
                'payment_notes': requests.POST.get('in_payment_notes').strip(),
            }

    data = {
        'number_of_tenants': number_of_tenants,
        'tenant_name_list': get_all_tenants()
    }
    if choice == 'add_tenant':
        return render(requests, 'homested/apartment/insert_tenant.html', {'data': data})
    
    if choice == 'bills':
        
        data['bills'] = query_nwc(os.getenv('CUSTOMER_NUMBER'), os.getenv('PREMISES_NUMBER'))
        
        return render(requests, 'homested/apartment/bills.html', {'data': data})
        
    return render(requests, 'homested/apartment/apartment.html', {'data': data})


@login_required(redirect_field_name=None, login_url='login/')
def files(requests):
    return render(requests, 'homested/files/files.html')


@login_required(redirect_field_name=None, login_url='login/')
def phone_home(requests):
    return render(requests, 'homested/phone_home/phone_home.html')


@login_required(redirect_field_name=None, login_url='login/')
def proxy(requests):
    return render(requests, 'homested/proxy/proxy.html')


def response_error_handler(requests, exception=None):
    return redirect('/')


def logout_user(requests):
    logout(requests)
    return redirect('/')


def login_user(requests):
    if requests.user.is_authenticated:
        return redirect('/')

    ip = get_user_ip(requests)

    if requests.method == 'POST':
        username = requests.POST['username']
        password = requests.POST['password']

        user = None
        try:
            user = authenticate(requests=requests, username=username, password=password)
            print(username, password)
        except:
            print('Invalid Credentials')
            logger.warning(
                f"Attempted Login from {format(ip)} username={username} password={password} {datetime.datetime.now()} ")

        if user is not None:
            login(requests, user)

    return render(requests, 'homested/login.html')
