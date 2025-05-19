from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils.text import slugify

from .models import Post
from .forms import PostForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True) # Показываем только опубликованные посты

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug' # Указываем, что используем slug для поиска объекта

    def get_object(self, queryset=None):
        # Получаем объект и увеличиваем счетчик просмотров
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:list') # Перенаправление после успешного создания

    def form_valid(self, form):
        # Автоматически генерируем slug, если он не был введен
        if not form.cleaned_data.get('slug'):
            form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug' # Указываем, что используем slug для поиска объекта

    def get_success_url(self):
        # Перенаправляем на страницу деталей поста после обновления
        return reverse_lazy('blog:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        # Автоматически генерируем slug, если он не был введен или изменился заголовок
        if not form.cleaned_data.get('slug') or form.cleaned_data.get('slug') != slugify(form.cleaned_data['title']):
             form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:list') # Перенаправление после успешного удаления
    context_object_name = 'post'
    slug_field = 'slug' # Указываем, что используем slug для поиска объекта
