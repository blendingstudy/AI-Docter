from django.urls import path

from .views import views

urlpatterns = [
    path('view/<str:view_name>', views.view, name='view'),
]