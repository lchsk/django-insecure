from django.urls import re_path

from . import views

urlpatterns = [
    re_path('unsafe/users/(?P<user_id>.*)', views.unsafe_users, name='unsafe_users'),
    re_path('safe/users/(?P<user_id>.*)', views.safe_users, name='safe_users'),

    re_path('files/read/(?P<filename>.*)', views.read_file, name='read_file'),
    re_path('files/copy/(?P<filename>.*)', views.copy_file, name='copy_file'),

    # insecure deserialization
    re_path('admin', views.admin_index, name='admin_index'),

    # XSS
    re_path('search', views.search, name='search'),
    re_path('log', views.log, name='log'),
]
