from django.urls import re_path

from plugins.ebsco_transporter import views


urlpatterns = [
    re_path(r'^manager/$', views.manager, name='ebsco_transporter_manager'),
]
