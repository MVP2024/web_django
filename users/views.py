from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView # Добавлено UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin # Добавлено
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import User
from .forms import CustomUserCreationForm, UserProfileEditForm # Добавлено UserProfileEditForm


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        subject = 'Добро пожаловать в Мир товаров!'
        message = (
            f'Здравствуйте, {user.first_name if user.first_name else user.email}!\n\n'
            'Спасибо за регистрацию на нашем сайте "Мир товаров".\n'
            'Теперь вы можете войти в свой аккаунт и пользоваться всеми функциями.\n\n'
            'С уважением,\nКоманда "Мир товаров"'
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            print(f"Приветственное письмо отправлено на {user.email}")
            messages.success(self.request, 'Вы успешно зарегистрированы! Пожалуйста, войдите.')
        except Exception as e:
            print(f"Ошибка при отправке приветственного письма на {user.email}: {e}")
            messages.error(self.request,
                       'Произошла ошибка при отправке приветственного письма. Пожалуйста, свяжитесь с поддержкой.')

        return response


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = AuthenticationForm
    next_page = reverse_lazy('catalog:home') # После успешного входа перенаправляем


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home') # Переанаправляем после выхода


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileEditForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile_edit')

    def get_object(self, queryset=None): # Изменено: добавлено queryset=None
        # Гарантируем, что пользователь может редактировать только свой собственный профиль
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Ваш профиль успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)