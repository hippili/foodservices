

from . import views
from django.conf.urls import url
from django.urls import path, re_path


app_name = 'crm'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/create/', views.customer_new, name='customer_new'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('service_list', views.service_list, name='service_list'),
    path('service/create/', views.service_new, name='service_new'),
    path('service/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('service/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('product_list', views.product_list, name='product_list'),
    path('product/create/', views.product_new, name='product_new'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('customer/<int:pk>/summary/', views.summary, name='summary'),
    path('customer/<int:pk>/export/', views.export_pdf, name='export_pdf'),
    path('product/<int:pk>/summary/', views.product_summary, name='product_summary'),
    path('service/<int:pk>/summary/', views.service_summary, name='service_summary'),

    path('product/<int:pk>/export/', views.product_export_pdf, name='product_export_pdf'),


]
