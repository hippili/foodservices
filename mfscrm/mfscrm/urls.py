"""mfscrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from . import views
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,\
     PasswordResetCompleteView,PasswordResetConfirmView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crm.urls')),
    re_path(r'^accounts/login/$', LoginView.as_view(template_name='registration/login.html'), name="login"),
    re_path(r'^accounts/logout/$', LogoutView.as_view(), LogoutView.next_page, name="logout"),
    url(r'^accounts/password-reset/$', PasswordResetView.as_view
    (template_name='registration/password_reset_form.html'), name='password-reset'),
    url(r'^accounts/password/reset/done/$', PasswordResetDoneView.as_view
    (template_name='registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$', PasswordResetCompleteView.as_view
    (template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    url(r'^signup/$', views.signup, name='signup'),



]
