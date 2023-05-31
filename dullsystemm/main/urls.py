from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from .views import *
from .models import Category, Product

urlpatterns = [
    path('', views.index, name='index'),  # Перешёл на главную страницу, показали ему функцию

    path('authorization/login/', LoginUser.as_view(), name='login'),  # Регистрация и авторизация на одной странице
    path('logout/', logout_user, name='logout'),  # выход пользователя
    path('registration/login/', RegisterUser.as_view(), name='register'),  # Форма помогает делать разные адреса
    path('reset_password/', password_reset_request,
         name='reset_password'),  # Переход на сброс пароля

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name='password_reset_done'),  # Показать сообщение, что Email ушел
    path('reset_password_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/reg.html"),
         name='password_reset_confirm'),  # Замена пароля
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done1.html"),
         name='password_reset_complete'),  # Пароль успешно изменен


    path('basket/', views.basket, name='basket'),  # Корзина
    path('products/', views.product, name='products'),  # Страница с товарами
    path('about_us/', views.about, name='about_us'),  # Страница о нас
    path('<int:id>/<slug:url_slug>', views.product_detail, name='product_detail'),  # отдельный товар c корзиной
    path('search/', Search.as_view(), name='search'),  # Поиск по аксессуарам
    path('<slug:slug>/', views.post_detail, name='post_detail'),  # Отзывы
    path('post/<slug:slug>/', views.news, name='news'),  # Новостная лента

]

if settings.DEBUG:  # включаем возможность обработки картинок
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
