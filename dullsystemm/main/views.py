from django.contrib.auth import logout, login  # Для авторизации на сайте
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import BadHeaderError, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterUserForm, LoginUserForm
from .models import Product

from .utils import *
from .forms import *

from cart.forms import CartAddProductForm


def index(request):
    Name_of_service = Prices.objects.all()  # Показываем цены при выпадающей окне
    Name_of_doctor = Doctor.objects.all()  # Информация о враче
    posts = Post_user.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')  # Отзывы
    news_post = Post_news.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')  # Новости
    price = list(Name_of_service)
    data = {
        'Name_of_service': price,
        'Name_of_doctor': Name_of_doctor,
        'posts': posts,
        'news_post': news_post,

    }

    return render(request, 'main./index.html', data)


def about(request):
    return render(request, 'main./about_us.html', )


def product(request):  # Для товаров

    category = Product.objects.all()
    product = Product.objects.filter(created__lte=timezone.now()).order_by('-created')  # Новости
    sorting_product = {'sorting': category,
                       'product': product,
                       }

    return render(request, 'products./products.html', sorting_product)


# Поиск по аксессуарам глаза
class Search(ListView):
    template_name = 'products/search.html'
    model = Product
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


def basket(request):  # Корзина
    category = Product.objects.all()

    sorting_product = {'sorting': category, }

    return render(request, 'main./basket.html', sorting_product)


# Авторизация пользователей

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'registration/registration.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):  # Для выхода из авторизации
    logout(request)
    return redirect('login')


# Регистрация пользователей

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация пользователя")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


# Cброс пароля
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            mail = password_reset_form.cleaned_data['email']
            try:
                user = User.objects.get(email=mail)  # email в форме регистрации проверен на уникальность
            except Exception:
                user = False
            if user:
                subject = 'Запрошен сброс пароля'
                email_template_name = "registration/password_reset_msg.html"
                cont = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',  # доменное имя сайта
                    'site_name': 'ГлазОК',  # ГлазОК
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),  # шифруем идентификатор
                    "user": user,  # чтобы обратиться в письме по логину пользователя
                    'token': default_token_generator.make_token(user),  # генерируем токен
                    'protocol': 'http',
                }
                msg_html = render_to_string(email_template_name, cont)
                try:
                    send_mail(subject, 'ссылка', 'admin@django-project.site', [user.email], fail_silently=True,
                              html_message=msg_html)
                except BadHeaderError:
                    return HttpResponse('Обнаружен недопустимый заголовок!')
                return redirect("/reset_password_sent/")
            else:
                return HttpResponse('Пользователь не найден, проверьте правильность вашей электронной почты')

    return render(request=request, template_name="registration/reset_password.html")


# Отзывы с комментариями

def post_detail(request, slug):
    template_name = 'comments/post_detail.html'
    post = get_object_or_404(Post_user, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Отзыв опубликован
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создать объект отзыва, но пока не сохранять в базе данных
            new_comment = comment_form.save(commit=False)
            # Назначить текущую публикацию отзыву
            new_comment.post = post
            # Сохранить отзыв в базе данных
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


def news(request, slug):
    news = Post_news.objects.filter(date_added__lte=timezone.now()).order_by('-date_added')  # Новости
    com = Comments_news.objects.select_related().filter(created_on__lte=timezone.now()).order_by(
        '-created_on')  # Новости

    template_name = 'comments/news.html'
    post_news = get_object_or_404(Post_news, slug=slug)
    comments = post_news.news_comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Комментарий опубликован
    if request.method == 'POST':
        comment_form = CommentFormNews(data=request.POST)  # Созданная форма
        if comment_form.is_valid():
            # Создать объект отзыва, но пока не сохранять в базе данных
            new_comment = comment_form.save(commit=False)
            # Назначить текущую публикацию
            new_comment.post = post_news
            # Сохранить коментарий в базе данных
            new_comment.save()
    else:
        comment_form = CommentFormNews()

    return render(request, template_name, {'post_news': post_news,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'news': news,
                                           'com': com,
                                           })

# Для корзины (не доделано)
def product_detail(request, id, url_slug):

    template_name = 'products/product_detail.html'
    product = get_object_or_404(Product, id=id, url_slug=url_slug, available=True)
    cart_product_form = CartAddProductForm()


    sorting_product = {'product': product,
                       'cart_product_form': cart_product_form, }

    return render(request, template_name, sorting_product)

# def name_of_the_page(request):
#  form = CartAddProductForm(request.POST or None)
#  answer = ''
#  if form.is_valid():
#   answer = form.cleaned_data.get('quantitye')

