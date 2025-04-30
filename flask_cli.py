from run import create_app
from app.config import Config
from flask_migrate import Migrate
from app.setup_db import db

# Создаём приложение
app = create_app(Config())

# Инициализируем миграции
migrate = Migrate(app, db)

# Запуск приложения для миграций
if __name__ == '__main__':
    app.run()
