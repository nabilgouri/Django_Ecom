from django.urls import path
from .views import itemList
app_name = 'core'
urlpatterns = [
    path('', itemList, name='item-list'),
]
