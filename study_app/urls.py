from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'study_app'

urlpatterns = [
    # Основные страницы
    path('', views.index, name='index'),
    path('student-choice/', views.student_choice, name='student_choice'),
    path('teacher-platform/', views.teacher_platform, name='teacher_platform'),
    path('camping-registration/', views.camping_registration, name='camping_registration'),
    path('about/', views.about, name='about'),
    
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='study_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Корзина
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:language_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),

    path('publish-article/', views.publish_article, name='publish_article'),
    path('teacher-notify/', views.teacher_notify, name='teacher_notify'),
]