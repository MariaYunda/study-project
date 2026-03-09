from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Language, Category, Course, Camping, CampingParticipant, Cart, CartItem, Article, Author, Module, Lesson
from .forms import CampingRegistrationForm, TeacherNotificationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def index(request):
    #Главная страница
    recent_articles = Article.objects.filter(is_published=True).order_by('-created_at')[:3]
    context = {
        'total_students': 15000,
        'total_courses': 50,
        'total_teachers': 120,
        'total_campings': 5,
        'recent_articles': recent_articles,
    }
    return render(request, 'study_app/index.html', context)

def student_choice(request):
    #Страница выбора курсов для студентов
    courses = Course.objects.filter(is_published=True).select_related('language', 'author')
    level = request.GET.get('level')
    if level and level != 'all':
        courses = courses.filter(level=level)
    
    context = {
        'courses': courses,
        'popular_languages': Language.objects.all(),
    }
    return render(request, 'study_app/student_choice.html', context)

def course_detail(request, course_slug):
    #Детальная страница курса
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    context = {
        'course': course,
    }
    return render(request, 'study_app/course_detail.html', context)

def teacher_platform(request):
    #Страница для преподавателей
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

def send_camping_confirmation_email(email, first_name, last_name, country):
    #Отправка подтверждения регистрации на кемпинг
    subject = '✅ Подтверждение регистрации на кемпинг Study.IT'
    
    # HTML письм0
    html_message = render_to_string('study_app/emails/camping_confirmation.html', {
        'first_name': first_name,
        'last_name': last_name,
        'country': country,
    })
    
    # текст письма
    text_message = f"""
Здравствуйте, {first_name} {last_name}!

Спасибо за регистрацию на кемпинг Study.IT в {country}!

Детали вашей регистрации:
- Имя: {first_name} {last_name}
- Страна кемпинга: {country}

В ближайшее время мы пришлем вам подробную информацию о программе, 
трансфере и проживании.

Следите за обновлениями на нашем сайте!

С уважением,
Команда Study.IT
"""
    
    send_mail(
        subject=subject,
        message=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=False,
    )

def camping_registration(request):
    if request.method == 'POST':
        form = CampingRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            if request.user.is_authenticated:
                registration.user = request.user
            registration.save()
            
            # Отправка email с подтверждением
            send_camping_confirmation_email(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                country=form.cleaned_data['desired_country']
            )
            
            messages.success(request, '✅ Вы успешно зарегистрированы на кемпинг! Проверьте вашу почту для получения подробной информации.')
            return redirect('study_app:camping_registration')
    else:
        form = CampingRegistrationForm()
    
    upcoming_campings = [
        {'country': 'Таиланд', 'dates': '15-30 июня 2026'},
        {'country': 'Грузия', 'dates': '10-25 июля 2026'},
        {'country': 'Португалия', 'dates': '5-20 августа 2026'},
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

# ==== СТАТЬИ ========

def article_list(request):
    #Страница со списком всех статей
    articles = Article.objects.filter(is_published=True).order_by('-created_at')
    context = {
        'articles': articles,
    }
    return render(request, 'study_app/article_list.html', context)

def article_detail(request, article_id):
    #Страница отдельной статьи
    article = get_object_or_404(Article, id=article_id, is_published=True)
    context = {
        'article': article,
    }
    return render(request, 'study_app/article_detail.html', context)

def publish_article(request):
    #Публикация статьи
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
        messages.success(request, '✅ Статья успешно опубликована!')
        return redirect('study_app:teacher_platform') 
    
    return redirect('study_app:teacher_platform')

# ======. КОРЗИНA ==========

def cart(request):
    #Страница корзины
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

def add_to_cart(request, language_id):
    #Добавление в корзину
    language = get_object_or_404(Language, id=language_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    course = Course.objects.filter(language=language).first()
    
    if not course:
        course = Course.objects.create(
            title=f"Изучение {language.name}",
            description=f'Полный курс по изучению {language.name} с нуля до профессионала',
            price=language.price or 5000,
            language=language,
            level='beginner',
            rating=4.5,
            is_published=True
        )
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, course=course)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'✅ Количество курсов "{language.name}" увеличено!')
    else:
        messages.success(request, f'✅ Курс "{language.name}" добавлен в корзину!')
    
    return redirect('study_app:student_choice')

def remove_from_cart(request, item_id):
    #Удаление товара из корзины
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
    #Обновление количества товара
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

def send_order_confirmation_email(email, cart_items, total):
    #Отправка подтверждения на почту
    subject = '✅ Подтверждение заказа - Study.IT'

    items_list = ''
    for item in cart_items:
        items_list += f"• {item.course.title} - {item.quantity} x {item.course.price} ₽ = {item.course.price * item.quantity} ₽\n"
    
    text_message = f"""
Здравствуйте!

Спасибо за заказ в Study.IT!

Детали вашего заказа:
{items_list}
Итого: {total} ₽

В ближайшее время мы свяжемся с вами для подтверждения заказа.

С уважением,
Команда Study.IT
"""
    
    send_mail(
        subject=subject,
        message=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

def checkout(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            messages.error(request, 'Пожалуйста, укажите email')
            return redirect('study_app:cart')
        
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_id = request.session.session_key
            cart = Cart.objects.filter(session_id=session_id).first()
        
        if cart and cart.items.exists():
            cart_items = cart.items.all()
            total = sum(item.course.price * item.quantity for item in cart_items)
            
            send_order_confirmation_email(
                email=email,
                cart_items=cart_items,
                total=total
            )
            
            cart.items.all().delete()
            
            messages.success(request, f'✅ Заказ успешно оформлен! Информация отправлена на {email}')
        else:
            messages.error(request, 'Корзина пуста')
            
        return redirect('study_app:cart')
    
    return redirect('study_app:cart')

def teacher_notify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, 'Спасибо! Мы уведомим вас о запуске.')
    return redirect('study_app:teacher_platform')