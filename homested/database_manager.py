from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect


def get_number_of_tenants():
    with connection.cursor() as cursor:
        cursor.execute("Select * FROM total_guests_view")
        connection.commit()
        number_of_tenants = cursor.fetchone()[0]

        if number_of_tenants > 0:
            return number_of_tenants
        else:
            return 0


def get_all_tenants():
    with connection.cursor() as cursor:
        cursor.execute("Select tenant_name FROM tenant ")
        connection.commit()
        tenant_list = cursor.fetchall()

        if tenant_list is not None:
            return tenant_list
        else:
            return 0


def insert_new_tenant():

    return 0