from django.contrib import admin
from .models import Language, Category, Course, Camping, CampingParticipant, Cart, CartItem

# Register your models here.

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'icon', 'color']
    list_editable = ['price']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'category', 'price', 'students_count', 'duration_hours']
    list_filter = ['language', 'category']
    search_fields = ['title', 'description']
    list_editable = ['price', 'students_count', 'duration_hours']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'language', 'category')
        }),
        ('Детали курса', {
            'fields': ('price', 'students_count', 'duration_hours')
        }),
    )

@admin.register(Camping)
class CampingAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'start_date', 'end_date', 'max_participants', 'current_participants', 'price']
    list_filter = ['location', 'start_date']
    search_fields = ['title', 'location', 'description']
    list_editable = ['price', 'max_participants', 'current_participants']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'location', 'description')
        }),
        ('Даты и участники', {
            'fields': ('start_date', 'end_date', 'max_participants', 'current_participants')
        }),
        ('Цена', {
            'fields': ('price',)
        }),
    )

@admin.register(CampingParticipant)
class CampingParticipantAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'country', 'desired_country', 'role', 'registered_at']
    list_filter = ['role', 'desired_country', 'registered_at']
    search_fields = ['first_name', 'last_name', 'email', 'country']
    readonly_fields = ['registered_at']
    
    fieldsets = (
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'country')
        }),
        ('Детали регистрации', {
            'fields': ('desired_country', 'role', 'user', 'registered_at')
        }),
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']
    fields = ['course', 'quantity', 'added_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'created_at', 'updated_at', 'get_items_count', 'get_total']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'session_id']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Количество товаров'
    
    def get_total(self, obj):
        total = sum(item.course.price * item.quantity for item in obj.items.all())
        return f'{total} ₽'
    get_total.short_description = 'Общая сумма'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'course', 'quantity', 'added_at', 'get_item_total']
    list_filter = ['added_at']
    search_fields = ['cart__id', 'course__title']
    readonly_fields = ['added_at']
    list_editable = ['quantity']
    
    def get_item_total(self, obj):
        total = obj.course.price * obj.quantity
        return f'{total} ₽'
    get_item_total.short_description = 'Сумма'