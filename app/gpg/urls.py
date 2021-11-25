from . import views
from django.urls import path


app_name = 'gpg'

urlpatterns = [
    path('decryptMessage/', views.decryptMessage, name='decryptMessage')
]
