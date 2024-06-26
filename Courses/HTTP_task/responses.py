import requests
import json

#Не смог получить 100ые и 500ые статусы по след. причинам
# Ответы 1xx (100-е коды)
# -Предназначение для информационного обмена: Коды статуса 100-е используются для промежуточных информационных ответов. Наиболее часто используется код 100 (Continue), который сообщает клиенту, что сервер получил начальную часть запроса и клиент может продолжить отправку оставшейся части.
# -Редко используются в реальной жизни: Хотя эти коды существуют, они используются редко. 
#  Клиенты и серверы в основном работают с кодами 200 и выше. Например, код 101 (Switching Protocols) используется для переключения протоколов, 
#  что также нечасто встречается.
# -Автоматическое управление: Большинство современных HTTP-библиотек и фреймворков автоматически управляют
#  промежуточными 1xx ответами, так что клиентские приложения редко видят эти коды напрямую.
# Ответы 5xx (500-е коды)
# -Серверные ошибки: Коды статуса 500-е означают, что на сервере произошла ошибка, которая мешает выполнению запроса. Например, 
#  код 500 (Internal Server Error) указывает на общую проблему на стороне сервера.
# -Предполагается стабильная работа сервера: В нормальных условиях серверы настроены и протестированы для стабильной работы, 
#  минимизируя возникновение ошибок. Администраторы и разработчики принимают меры по предотвращению сбоев.
# -Обработка ошибок: Современные серверные системы часто имеют механизмы для обработки и логирования ошибок,
#  а также для возврата клиентам более дружественных сообщений об ошибках, что может скрывать исходные 500-е коды.
# Примеры:
# 100 (Continue): Клиент отправляет запрос с большой загрузкой данных и ожидает подтверждения от сервера, что можно продолжать отправку.
# 500 (Internal Server Error): Сервер не может обработать запрос из-за внутренней ошибки, например, из-за сбоя в работе кода или базы данных.
# Таким образом, в обычной ситуации коды 100 и 500 встречаются реже из-за специфичности их применения и мер по предотвращению ошибок на сервере.

url_reqres = "https://reqres.in/api"
url_json_place = 'https://jsonplaceholder.typicode.com'
url_httpbin = 'https://httpbin.org/status/502'

request_OK = requests.request("GET",f'{url_reqres}/users?page=2')

request_Created = requests.request("POST",f'{url_json_place}/posts', 
                                    data = json.dumps(
                                    {"title": "foo",
                                    "body": "bar",
                                    "userId": 1
                                    }),
                                    headers = 
                                    {'Content-Type': 'application/json'})

request_No_Content = requests.request('DELETE', f'{url_reqres}/users')

request_Not_Found = requests.request('GET', f'{url_reqres}/users/23')

request_Bad_Request = requests.request('POST', f'{url_reqres}/register', 
                                        data=json.dumps(
                                            {"email": "sydney@fife"}),
                                        headers = {'Content-Type': 'application/json'})

request_Moved_Permanently = requests.request('GET', url='http://github.com', allow_redirects=False)


print(f'Successful Response - {request_OK.status_code}\n',
      f'Successful Response - {request_Created.status_code}\n',
      f'Redirect Response - {request_Moved_Permanently.status_code}\n',
      f'ErrorClient Response - {request_Bad_Request.status_code}\n',
      f'ErrorClient Response - {request_Not_Found.status_code}\n'
      )


