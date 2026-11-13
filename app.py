from database import get_db, init_db
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)

app.secret_key = "my_secret_key"

init_db()

@app.route("/")
def index():
    return redirect(url_for("register"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db()

        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        connection.commit()
        connection.close()

        flash("Регистрация прошла успешно!")

        return redirect(url_for("register"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db()
        
        # query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        # user = connection.execute(query).fetchone()

        # Исправление SQL Injection
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = connection.execute(
            query,
            (username, password)
        ).fetchone()

        connection.close()

        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("profile", user_id=user["id"]))
        else:
            flash("Неверный логин или пароль!")

        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/profile/<int:user_id>")
def profile(user_id):
    # Исправление IDOR
    if "user_id" not in session:
        return redirect(url_for("login"))

    if session["user_id"] != user_id:
        return "Доступ запрещён!", 403

    connection = get_db()

    user = connection.execute(
        "SELECT id, username, password FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    connection.close()

    if user is None:
        return "Пользователь не найден", 404

    return render_template("profile.html", user=user)

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    flash("Вы вышли из аккаунта!")

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
