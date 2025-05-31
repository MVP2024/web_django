from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Загружает тестовые данные из фикстуры после очистки существующих данных"

    def handle(self, *args, **options):
        self.stdout.write("Удаление существующих данных...")
        # Удаляем данные из моделей Product и Category
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Существующие данные удалены."))

        self.stdout.write("Загрузка данных из фикстуры...")
        # Загружаем данные из фикстуры
        call_command("loaddata", "initial_data")
        self.stdout.write(self.style.SUCCESS("Данные успешно загружены."))
