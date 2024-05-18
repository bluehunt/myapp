from django.urls import path
from . import views

urlpatterns = [
    path('food', views.food,name='food'),
    path('', views.foods,name='foods'),
]