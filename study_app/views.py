from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Language, Category, Course, Camping, CampingParticipant, Cart, CartItem
from .forms import CampingRegistrationForm, TeacherNotificationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Article 

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
    languages = Language.objects.all()
    context = {
        'popular_languages': languages,
    }
    return render(request, 'study_app/student_choice.html', context)

def teacher_platform(request):
    """Страница для преподавателей"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, 'Спасибо! Мы уведомим вас о запуске.')
            return redirect('study_app:teacher_platform')
    return render(request, 'study_app/teacher_platform.html')

def camping_registration(request):
    """Страница регистрации на кемпинг"""
    if request.method == 'POST':
        form = CampingRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            if request.user.is_authenticated:
                registration.user = request.user
            registration.save()
            messages.success(request, 'Вы успешно зарегистрированы на кемпинг! Мы отправили подробности на ваш email.')
            return redirect('study_app:camping_registration')
    else:
        form = CampingRegistrationForm()
    
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

def about(request):
    """Страница о нас"""
    return render(request, 'study_app/about.html')

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('study_app:index')
    else:
        form = UserCreationForm()
    return render(request, 'study_app/register.html', {'form': form})

# ========== ФУНКЦИИ ДЛЯ КОРЗИНЫ ==========

def cart(request):
    """Страница корзины"""
    # Получаем или создаем корзину
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    cart_items = cart.items.all()
    total = sum(item.course.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'study_app/cart.html', context)

# def add_to_cart(request, language_id):
#     """Добавление языка в корзину"""
#     language = get_object_or_404(Language, id=language_id)
    
#     # Получаем или создаем корзину
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         session_id = request.session.session_key
#         if not session_id:
#             request.session.create()
#             session_id = request.session.session_key
#         cart, created = Cart.objects.get_or_create(session_id=session_id)
    
#     # Создаем временный курс для языка
#     course, created = Course.objects.get_or_create(
#         title=f"Изучение {language.name}",
#         defaults={
#             'description': f'Полный курс по изучению {language.name} с нуля до профессионала',
#             'price': language.price or 5000,
#             'language': language
#         }
#     )
    
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)
    
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
    
#     messages.success(request, f'Курс по {language.name} добавлен в корзину')
#     return redirect('study_app:student_choice')

def add_to_cart(request, language_id):
    """Добавление языка в корзину"""
    language = get_object_or_404(Language, id=language_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    course, created = Course.objects.get_or_create(
        title=f"Изучение {language.name}",
        defaults={
            'description': f'Полный курс по изучению {language.name} с нуля до профессионала',
            'price': language.price or 5000,
            'language': language
        }
    )
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество курсов "{language.name}" увеличено!')
    else:
        messages.success(request, f'Курс "{language.name}" добавлен в корзину!')
    
    return redirect('study_app:student_choice')

def remove_from_cart(request, item_id):
    """Удаление товара из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.user.is_authenticated:
        if cart_item.cart.user != request.user:
            messages.error(request, 'Доступ запрещен')
            return redirect('study_app:cart')
    else:
        session_id = request.session.session_key
        if cart_item.cart.session_id != session_id:
            messages.error(request, 'Доступ запрещен')
            return redirect('study_app:cart')
    
    course_title = cart_item.course.title
    cart_item.delete()
    
    messages.success(request, f'"{course_title}" удален из корзины')
    return redirect('study_app:cart')

def update_cart_quantity(request, item_id):
    """Обновление количества товара"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Количество обновлено')
        else:
            messages.error(request, 'Количество должно быть больше 0')
    
    return redirect('study_app:cart')

def checkout(request):
    """Оформление заказа"""
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_id = request.session.session_key
            cart = Cart.objects.filter(session_id=session_id).first()
        
        if cart:
            cart.items.all().delete()
        
        messages.success(request, '✅ Заказ успешно оформлен! Скоро мы свяжемся с вами.')
        return redirect('study_app:cart')
    
    return redirect('study_app:cart')

def teacher_platform(request):
    """Страница для преподавателей"""
    recent_articles = Article.objects.filter(is_published=True).order_by('-created_at')[:3]
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, 'Спасибо! Мы уведомим вас о запуске.')
            return redirect('study_app:teacher_platform')
    
    context = {
        'recent_articles': recent_articles,
    }
    return render(request, 'study_app/teacher_platform.html', context)

def publish_article(request):
    """Публикация статьи"""
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        excerpt = request.POST.get('excerpt')
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')
        
        article = Article(
            title=title,
            category=category,
            excerpt=excerpt,
            content=content,
            tags=tags,
            author=request.user if request.user.is_authenticated else None
        )
        
        if 'image' in request.FILES:
            article.image = request.FILES['image']
        
        article.save()
        messages.success(request, 'Статья успешно опубликована!')
        return redirect('study_app:teacher_platform')
    
    return redirect('study_app:teacher_platform')

def teacher_notify(request):
    """Уведомление преподавателя"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, 'Спасибо! Мы уведомим вас о запуске.')
    return redirect('study_app:teacher_platform')