from flask import Flask

# Импортируется нужный класс:
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключаем БД SQLite:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# Создаётся экземпляр класса SQLAlchemy и передаётся
# в качестве параметра экземпляр приложения Flask:
db = SQLAlchemy(app)


@app.route('/')
def index_view():
    return 'Совсем скоро тут будет случайное мнение о фильме!'


if __name__ == '__main__':
    app.run()
