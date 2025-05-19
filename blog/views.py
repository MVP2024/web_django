from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    """
    Представление для отображения списка опубликованных записей блога.
    """

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    """
    Представление для отображения одной записи блога.
    Увеличивает счетчик просмотров и отправляет email при достижении 100 просмотров.
    """

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    pk_url_kwarg = "pk"

    def get_object(self, queryset=None):
        """
        Получает объект записи блога, увеличивает счетчик просмотров
        и отправляет email, если достигнуто 100 просмотров.
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        if self.object.views_count == 100:
            subject = f'Поздравляем! Статья "{self.object.title}" достигла 100 просмотров!'
            # Используем self.object.pk для генерации URL
            message = (
                f'Ваша статья "{self.object.title}" набрала 100 просмотров.\n\n'
                f"Ссылка на статью: "
                f'{self.request.build_absolute_uri(reverse_lazy("blog:detail", kwargs={"pk": self.object.pk}))}'
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                print(f"Email отправлен: Статья '{self.object.title}' достигла 100 просмотров.")
            except Exception as e:
                print(f"Ошибка при отправке email: {e}")

        return self.object


class PostCreateView(CreateView):
    """
    Представление для создания новой записи блога.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:list")


class PostUpdateView(UpdateView):
    """
    Представление для редактирования существующей записи блога.
    """

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    pk_url_kwarg = "pk"

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления записи.
        Перенаправляет на страницу деталей обновленной записи.
        """
        # Используем self.object.pk для перенаправления
        return reverse_lazy("blog:detail", kwargs={"pk": self.object.pk})


class PostDeleteView(DeleteView):
    """
    Представление для удаления записи блога.
    """

    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
    context_object_name = "post"
    pk_url_kwarg = "pk"
