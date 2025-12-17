
from django.urls import path

from tracker import views

urlpatterns = [
    path('',views.index,name='index'),
    path('delete-history/<int:id>',views.delete_history,name='delete_history'),
    path('login/',views.login_view,name='login_view'),
    path('register/',views.register_view,name='register_view'),
    path('logout/',views.logout_view,name='logout_view'),
]