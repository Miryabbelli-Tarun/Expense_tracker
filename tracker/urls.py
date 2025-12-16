
from django.urls import path

from tracker import views

urlpatterns = [
    path('',views.index,name='index'),
    path('delete-history/<int:id>',views.delete_history,name='delete_history')
]