"""
This file holds all urls used by RequestManager application
"""
from django.urls import path
from . import views

app_name = 'RequestManager'
urlpatterns = [
    # Index URL, home page
    path('', views.home, name='home'),
    # New Request URL, use to submit request
    path('new_request/', views.new_request, name='new_request'),
    # Operation result page, use to show error after operation fail
    path('request_result/?error=<str:error>', views.request_result, name='request_result_error'),
    # Operation result page, use to show status after operation success
    path('request_result/?status=<str:status>', views.request_result, name='request_result_ok'),
    # All request page, show all submited request
    # page parameter: requests splited into page, every page has 12 items
    path('all_requests/?page=<int:page>', views.all_requests, name='all_requests'),
    # Detail of each request
    # Parameter: id of the request
    path('request/<int:pk>/', views.RequestView.as_view(), name='detail'),
    # Edit request page, only accessible via post request
    path('request/edit', views.edit_request, name='edit_request'),
    # Delete request page, only accessible via post request
    path('request/delete', views.delete_request, name='delete_request'),
    # Show trivia information about my self
    path('about/', views.about, name='about'),
    # Register url
    path('register/', views.register, name='Register'),
]
