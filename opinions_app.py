from datetime import datetime

# Импортируется функция для выбора случайного значения:
from random import randrange

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключаем БД SQLite:
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
# Создаётся экземпляр класса SQLAlchemy и передаётся
# в качестве параметра экземпляр приложения Flask:
db = SQLAlchemy(app)


class Opinion(db.Model):
    # ID — целое число, первичный ключ:
    id = db.Column(db.Integer, primary_key=True)
    # Название фильма — строка длиной 128 символов, не может быть пустым:
    title = db.Column(db.String(128), nullable=False)
    # Мнение о фильме — большая строка, не может быть пустым,
    # должно быть уникальным:
    text = db.Column(db.Text, unique=True, nullable=False)
    # Ссылка на сторонний источник — строка длиной 256 символов:
    source = db.Column(db.String(256))
    # Дата и время — текущее время,
    # по этому столбцу база данных будет проиндексирована:
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


@app.route("/")
def index_view():
    # Определяется количество мнений в базе данных:
    quantity = Opinion.query.count()
    # Если мнений нет...
    if not quantity:
        # ...то возвращается сообщение:
        return "В базе данных мнений о фильмах нет."
    # Иначе выбирается случайное число в диапазоне от 0 до quantity...
    offset_value = randrange(quantity)
    # ...и определяется случайный объект:
    # Извлекаем все записи, пропуская первые offset_value записей,
    # и берём первую запись из получившегося набора:
    opinion = Opinion.query.offset(offset_value).first()
    # Тут подключаем шаблон opinion.html:
    return render_template("opinion.html", opinion=opinion)


@app.route("/add")
def add_opinion_view():
    # Тут подключаем шаблон add_opinion.html:
    return render_template("add_opinion.html")


# Тут указывается конвертер пути для id:
@app.route("/opinions/<int:id>")
# Параметром указывается имя переменной:
def opinion_view(id):
    # Теперь можно запросить нужный объект по id...
    # opinion = Opinion.query.get(id)
    # Метод get() заменён на get_or_404():
    opinion = Opinion.query.get_or_404(id)
    # ...и передать его в шаблон (шаблон тот же, что и для главной страницы):
    return render_template("opinion.html", opinion=opinion)


if __name__ == "__main__":
    app.run()
