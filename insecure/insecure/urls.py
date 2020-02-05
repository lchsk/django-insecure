from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('security/', include('security.urls')),
    path('admin/', admin.site.urls),
]
