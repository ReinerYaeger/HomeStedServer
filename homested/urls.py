from django.urls import path
from . import views
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', views.index, name='index'),
    path('apartment/', views.apartment, name='apartment'),
    path('apartment/<str:choice>/',views.apartment,name='apartment'),
    path('apartment/<str:choice>/',views.apartment,name='apartment'),
    path('files/', views.files, name='files'),
    path('proxy/', views.proxy, name='proxy'),
    path('phone_home/', views.phone_home, name='phone_home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]

handler404 = views.response_error_handler
handler500 = views.response_error_handler
handler403 = views.response_error_handler
