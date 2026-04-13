
from django.urls import path
from . views import *

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('submit-code/', views.submit_code_view, name='submit_code'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('review-result/<int:review_id>/', views.review_result_view, name='review_result'),
    path('review-history/', views.review_history_view, name='review_history'),
    path('profile/', views.profile_view, name='profile'),
]