
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('gpg.urls', namespace='gpg')),
    path('admin/', admin.site.urls),
]
