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

                # Получаем данные из запроса
                request_data = b""
                while True:
                    chunk = conn.recv(1024)
                    request_data += chunk
                    # Проверяем, получили ли мы конец заголовков (\r\n\r\n)
                    if b'\r\n\r\n' in request_data:
                        break
                    # Если chunk меньше 1024, возможно, это конец запроса без тела
                    if len(chunk) < 1024:
                         break


                request_str = request_data.decode('utf-8', errors='ignore')
                print(f"Получен запрос:\n{request_str}")

                # Парсим первую строку запроса для определения метода
                request_lines = request_str.split('\r\n')
                if not request_lines:
                    conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                    continue

                first_line = request_lines[0]
                parts = first_line.split()
                if len(parts) < 3:
                    conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
                    continue

                method, path, http_version = parts
                print(f"Метод запроса: {method}")
                print(f"Путь запроса: {path}")

                if method == 'POST':
                    # Если это POST-запрос, ищем заголовок Content-Length
                    headers = {}
                    body_start_index = request_data.find(b'\r\n\r\n') + 4
                    header_lines = request_lines[1:request_lines.index('')] # Получаем строки заголовков

                    for line in header_lines:
                        if ': ' in line:
                            key, value = line.split(': ', 1)
                            headers[key.lower()] = value.strip()

                    content_length = int(headers.get('content-length', 0))
                    print(f"Ожидаемая длина тела POST-запроса: {content_length} байт")

                    # Читаем оставшееся, если она не была получена с заголовками
                    body_data = request_data[body_start_index:]
                    remaining_to_read = content_length - len(body_data)

                    while remaining_to_read > 0:
                        chunk = conn.recv(min(remaining_to_read, 1024))
                        if not chunk:
                            break # Соединение закрыто
                        body_data += chunk
                        remaining_to_read -= len(chunk)

                    # Декодируем и выводим тело запроса
                    try:
                        post_body = body_data.decode('utf-8')
                        print(f"Полученные данные POST-запроса:\n{post_body}")
                    except UnicodeDecodeError:
                        print("Не удалось декодировать тело POST-запроса как UTF-8")
                        print(f"Тело запроса (байты):\n{body_data}")


                    # Отправляем простой ответ на POST-запрос
                    response_body = "Данные POST получены успешно!"
                    status_line = "HTTP/1.1 200 OK\r\n"
                    content_type = "Content-Type: text/plain; charset=utf-8\r\n"
                    content_length_header = f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
                    response = f"{status_line}{content_type}{content_length_header}\r\n{response_body}"
                    conn.sendall(response.encode('utf-8'))

                else: # Обрабатываем другие методы (например, GET)
                    # Читаем содержимое HTML файла
                    try:
                        with open('contacts.html', 'r', encoding='utf-8') as f:
                            html_content = f.read()
                    except FileNotFoundError:
                        # Если файл не найден, отправляем ошибку 404
                        html_content = "<h1>Ошибка 404: Файл не найден</h1>"
                        status_line = "HTTP/1.1 404 Not Found\r\n"
                        content_type = "Content-Type: text/html; charset=utf-8\r\n"
                        content_length_header = f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
                        response = f"{status_line}{content_type}{content_length_header}\r\n{html_content}"
                        conn.sendall(response.encode('utf-8'))
                        continue # Переходим к следующему соединению

                    # Формируем HTTP-ответ для HTML
                    status_line = "HTTP/1.1 200 OK\r\n"
                    content_type = "Content-Type: text/html; charset=utf-8\r\n"
                    content_length_header = f"Content-Length: {len(html_content.encode('utf-8'))}\r\n" # Длина содержимого в байтах

                    # Собираем полный ответ: статус, заголовки, пустая строка, содержимое
                    response = f"{status_line}{content_type}{content_length_header}\r\n{html_content}"

                    # Отправляем ответ клиенту (кодируем строку в байты)
                    conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    run_server()
