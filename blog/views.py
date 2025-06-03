from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin # Импортируем миксин

from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count == 100:
            subject = f'Поздравляем! Статья "{self.object.title}" достигла 100 просмотров!'
            message = f'Ваша статья "{self.object.title}" набрала 100 просмотров.\n\nСсылка на статью: {self.request.build_absolute_uri(reverse_lazy("blog:detail", kwargs={"pk": self.object.pk}))}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                print(f"Email отправлен: Статья '{self.object.title}' достигла 100 просмотров.")
            except Exception as e:
                print(f"Ошибка при отправке email: {e}")

        return self.object


class PostCreateView(LoginRequiredMixin, CreateView): # Добавляем LoginRequiredMixin
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:list')


class PostUpdateView(LoginRequiredMixin, UpdateView): # Добавили LoginRequiredMixin
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView): # Добавили LoginRequiredMixin
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    context_object_name = 'post'
    pk_url_kwarg = 'pk'