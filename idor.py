
import requests

BASE_URL = "http://127.0.0.1:5000"

session = requests.Session()


login_data = {
    "username": "test1",
    "password": "123"
}

login_response = session.post(
    f"{BASE_URL}/login",
    data=login_data,
    allow_redirects=False
)
print('-' * 40)
print("Вход в аккаунт:", login_response.status_code)

response = session.get(f"{BASE_URL}/profile/1")

print("Проверка IDOR")
print("Код ответа:", response.status_code)

if response.status_code == 200:
    print("Профиль доступен.")
elif response.status_code == 403:
    print("Доступ запрещён. IDOR исправлена.")
elif response.status_code == 302:
    print("Перенаправление на страницу входа.")
else:
    print("Получен другой ответ.")

print("-" * 40)
