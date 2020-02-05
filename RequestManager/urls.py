from django.urls import path
from . import views

app_name = 'RequestManager'
urlpatterns = [
    path('', views.home, name='home'),
    path('new_request/', views.new_request, name='new_request'),
    path('request_result/', views.request_result, name='request_result'),
    path('all_requests/?page=<int:page>', views.all_requests, name='all_requests'),
    path('request/<int:pk>/', views.RequestView.as_view(), name='detail'),
    path('request/edit', views.edit_request, name='edit_request'),
    path('request/delete', views.delete_request, name='delete_request'),
    path('about/', views.about, name='about')
]
