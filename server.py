import socket

HOST = '127.0.0.1'  # Стандартный адрес локального хоста
PORT = 8000         # Порт для прослушивания (можно выбрать любой свободный)

def run_server():
    # Создаем сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Привязываем сокет к адресу и порту
        s.bind((HOST, PORT))
        # Начинаем прослушивать входящие соединения
        s.listen()

        print(f"Сервер запущен и слушает на {HOST}:{PORT}")

        while True:
            # Принимаем входящее соединение
            conn, addr = s.accept()
            with conn:
                print(f"Подключено клиентом: {addr}")

                # Получаем данные из запроса (для простоты не парсим его полностью)
                request = conn.recv(1024).decode('utf-8')
                # print(f"Получен запрос:\n{request}") # Раскомментируйте для отладки

                # Читаем содержимое HTML файла
                try:
                    with open('contacts.html', 'r', encoding='utf-8') as f:
                        html_content = f.read()
                except FileNotFoundError:
                    # Если файл не найден, отправляем ошибку 404
                    html_content = "<h1>Ошибка 404: Файл не найден</h1>"
                    status_line = "HTTP/1.1 404 Not Found\r\n"
                    content_type = "Content-Type: text/html; charset=utf-8\r\n"
                    content_length = f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
                    response = f"{status_line}{content_type}{content_length}\r\n{html_content}"
                    conn.sendall(response.encode('utf-8'))
                    continue # Переходим к следующему соединению

                # Формируем HTTP-ответ
                status_line = "HTTP/1.1 200 OK\r\n"
                content_type = "Content-Type: text/html; charset=utf-8\r\n" # Указываем Content-Type как text/html
                content_length = f"Content-Length: {len(html_content.encode('utf-8'))}\r\n" # Длина содержимого в байтах

                # Собираем полный ответ: статус, заголовки, пустая строка, содержимое
                response = f"{status_line}{content_type}{content_length}\r\n{html_content}"

                # Отправляем ответ клиенту (кодируем строку в байты)
                conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    run_server()
