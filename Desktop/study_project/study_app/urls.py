from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'study_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('student-choice/', views.student_choice, name='student_choice'),
    path('teacher-platform/', views.teacher_platform, name='teacher_platform'),
    path('camping-registration/', views.camping_registration, name='camping_registration'),
    path('courses/', views.course_list, name='course_list'),
    path('about/', views.about, name='about'),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='study_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]