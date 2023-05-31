from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

admin.site.register(Prices)
admin.site.register(Category)
admin.site.register(Doctor)


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    readonly_fields = ("get_image",)
    extra = 1

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="130" height="110"')  # Показываем изображение внутри товара

    get_image.short_description = "Изображение"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [GalleryInline, ]
    readonly_fields = ("get_image",)  # Показываем изображение в панели администратора

    list_display = (
    'id', 'name', 'slug', 'pubdate', 'optical', 'radius', 'price', 'stock', 'available', 'created', 'updated',
    'get_image', )
    list_filter = ['category', 'price', 'created', 'updated', 'name', 'radius', 'optical', ]
    prepopulated_fields = {'url_slug': ('name',)}
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="30"')

    get_image.short_description = "Вид товара"


@admin.register(Post_user)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'date_added', 'slug', 'title')
    list_filter = ('author', 'date_added', 'slug')
    search_fields = ('author', 'date_added')
    prepopulated_fields = {'slug': ('title',)}


    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(Comments_User)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'body', 'created_on', 'active', 'author_name')
    list_filter = ('active', 'created_on')
    search_fields = ('username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Post_news)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'date_added', 'slug', 'title')
    list_filter = ('author', 'date_added', 'slug')
    search_fields = ('author', 'date_added')
    prepopulated_fields = {'slug': ('title',)}


    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(Comments_news)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_news', 'username', 'body', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)