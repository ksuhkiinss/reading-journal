from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret_key"

# 🔹 Налаштування LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# 🔹 Абсолютний шлях до бази даних
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 🔹 Клас користувача
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    if user:
        return User(user["id"], user["username"])
    return None

# 🔹 Реєстрація
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed = generate_password_hash(password)

        db = get_db()
        # Перевіряємо, чи користувач вже існує
        existing = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            db.close()
            return "Користувач вже існує! Спробуй інше ім'я."
        
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        db.commit()
        db.close()

        return redirect("/login")

    return render_template("register.html")

# 🔹 Вхід
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            login_user(User(user[0], user[1]))
            return redirect("/")

        return "Неправильне ім'я користувача або пароль."

    return render_template("login.html")

# 🔹 Головна сторінка (треба логін)
@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

# 🔹 Вихід
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
