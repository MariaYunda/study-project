from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Language, Category, Course, Camping, CampingParticipant
from .forms import CampingRegistrationForm, TeacherNotificationForm

def index(request):
    """Главная страница"""
    context = {
        'total_students': 15000,
        'total_courses': 50,
        'total_teachers': 120,
        'total_campings': 5,
    }
    return render(request, 'study_app/index.html', context)

def student_choice(request):
    """Страница выбора языка для студентов"""
    # Популярные языки (можно заменить на реальные данные из БД)
    popular_languages = [
        {'name': 'Python', 'icon': 'fab fa-python', 'color': '#3776AB', 'slug': 'python'},
        {'name': 'JavaScript', 'icon': 'fab fa-js', 'color': '#F7DF1E', 'slug': 'javascript'},
        {'name': 'Java', 'icon': 'fab fa-java', 'color': '#007396', 'slug': 'java'},
        {'name': 'C++', 'icon': 'fas fa-code', 'color': '#00599C', 'slug': 'cpp'},
        {'name': 'PHP', 'icon': 'fab fa-php', 'color': '#777BB4', 'slug': 'php'},
        {'name': 'Ruby', 'icon': 'fas fa-gem', 'color': '#CC342D', 'slug': 'ruby'},
    ]
    
    # Все категории
    categories = [
        {'name': 'Веб-разработка', 'icon': 'fas fa-globe', 'slug': 'web', 'courses': 15},
        {'name': 'Мобильная разработка', 'icon': 'fas fa-mobile-alt', 'slug': 'mobile', 'courses': 8},
        {'name': 'Data Science', 'icon': 'fas fa-chart-bar', 'slug': 'data', 'courses': 12},
        {'name': 'DevOps', 'icon': 'fas fa-server', 'slug': 'devops', 'courses': 6},
        {'name': 'GameDev', 'icon': 'fas fa-gamepad', 'slug': 'gamedev', 'courses': 5},
        {'name': 'Кибербезопасность', 'icon': 'fas fa-shield-alt', 'slug': 'security', 'courses': 4},
    ]
    
    context = {
        'popular_languages': popular_languages,
        'categories': categories,
    }
    return render(request, 'study_app/student_choice.html', context)

def teacher_platform(request):
    """Страница для преподавателей"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Здесь можно сохранить email в базу данных для уведомлений
            messages.success(request, 'Спасибо! Мы уведомим вас о запуске.')
            return redirect('study_app:teacher_platform')
    
    return render(request, 'study_app/teacher_platform.html')

def camping_registration(request):
    """Страница регистрации на кемпинг"""
    if request.method == 'POST':
        form = CampingRegistrationForm(request.POST)
        if form.is_valid():
            # Сохраняем регистрацию
            registration = form.save(commit=False)
            if request.user.is_authenticated:
                registration.user = request.user
            registration.save()
            messages.success(request, 'Вы успешно зарегистрированы на кемпинг! Мы отправили подробности на ваш email.')
            return redirect('study_app:camping_registration')
    else:
        form = CampingRegistrationForm()
    
    # Получаем ближайшие кемпинги
    upcoming_campings = [
        {'country': 'Таиланд', 'dates': '15-30 июня 2024'},
        {'country': 'Грузия', 'dates': '10-25 июля 2024'},
        {'country': 'Португалия', 'dates': '5-20 августа 2024'},
    ]
    
    context = {
        'form': form,
        'upcoming_campings': upcoming_campings,
    }
    return render(request, 'study_app/camping_registration.html', context)

def course_list(request):
    """Список курсов (для фильтрации)"""
    category = request.GET.get('category')
    # Здесь будет логика фильтрации курсов по категории
    return render(request, 'study_app/course_list.html')

def about(request):
    """Страница о нас"""
    return render(request, 'study_app/about.html')