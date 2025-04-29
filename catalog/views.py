from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f'Получено сообщение от {name}: телефон: {phone} и сообщение: {message}')

        return render(request, 'contacts.html', {'name': name, 'phone': phone, 'message': message})

    # Если метод запроса GET, то просто выводим страницу контактов
    return render(request, 'contacts.html')
