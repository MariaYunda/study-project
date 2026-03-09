from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Language(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(default='', blank=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='Имя автора')
    bio = models.TextField(blank=True, verbose_name='Биография')
    avatar = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name='Аватар')
    experience = models.IntegerField(default=0, verbose_name='Лет опыта')
    students_count = models.IntegerField(default=0, verbose_name='Количество студентов')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')
    description = models.TextField(default='', blank=True, verbose_name='Описание')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name='Язык')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Изображение')
    
    # Статистика
    students_count = models.IntegerField(default=0, verbose_name='Количество студентов')
    rating = models.FloatField(default=0.0, verbose_name='Рейтинг')
    duration_hours = models.IntegerField(default=10, verbose_name='Длительность (часы)')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name='Уровень')
    
    # Dанные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название модуля')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', verbose_name='Модуль')
    title = models.CharField(max_length=200, verbose_name='Название урока')
    content = models.TextField(blank=True, verbose_name='Содержание')
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    duration_minutes = models.IntegerField(default=0, verbose_name='Длительность (минуты)')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_free = models.BooleanField(default=False, verbose_name='Бесплатный урок')
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
    
    def __str__(self):
        return self.title

class Camping(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    max_participants = models.IntegerField(default=30)
    current_participants = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(default='', blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.location}"

class CampingParticipant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    desired_country = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    camping = models.ForeignKey(Camping, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.desired_country}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} in cart {self.cart.id}"
    

class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []