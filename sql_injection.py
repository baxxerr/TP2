import requests

URL = "http://127.0.0.1:5000/login"

session = requests.Session()


def test_login(username, password):
    response = session.post(
        URL,
        data={
            "username": username,
            "password": password
        },
        allow_redirects=False
    )
    print("-" * 40)

    print("Логин:", username)
    print("Код ответа:", response.status_code)
    print("Перенаправление:", response.headers.get("Location"))

    if response.status_code == 302:
        print("Сервер выполнил перенаправление после входа.")

    print("-" * 40)

test_login("admin", "123")
test_login("test1", "123")
test_login("wrong_user' OR '1' == '1' --", "wrong_password")


