from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^register_exist/$', views.register_exist, name='register_exist'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_handle/$', views.login_handle, name='login_handle'),
    url(r'^info/$', views.info),
    url(r'^site/$', views.site),
    url(r'^logout/$', views.logout),
    url(r'^user_center_order&(\d+)/$', views.user_center_order)
]