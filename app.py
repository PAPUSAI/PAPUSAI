import os
import random
import sqlite3
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
# Используем папку /tmp, так как на бесплатных хостингах файлы можно создавать только там
DB_PATH = "/tmp/pvxen.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            standoff_id TEXT NOT NULL,
            custom_id_2 TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def generate_custom_id():
    return f"PVX-{random.randint(1000, 9999)}"


@app.route("/")
def index():
    init_db()  # Проверяем бд при каждом заходе
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nickname, standoff_id, custom_id_2 FROM players")
    players = cursor.fetchall()
    conn.close()
    return render_template("index.html", players=players)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if request.method == "POST":
        nickname = request.form.get("nickname")
        standoff_id = request.form.get("standoff_id")
        custom_id_2 = generate_custom_id()

        if nickname and standoff_id:
            cursor.execute(
                "INSERT INTO players (nickname, standoff_id, custom_id_2) VALUES (?, ?, ?)",
                (nickname, standoff_id, custom_id_2),
            )
            conn.commit()
        return redirect(url_for("admin"))

    cursor.execute("SELECT id, nickname, standoff_id, custom_id_2 FROM players")
    players = cursor.fetchall()
    conn.close()
    return render_template("admin.html", players=players)


if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
