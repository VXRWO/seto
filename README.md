# СЭТО — Веб-приложение аренды помещений (Django)

Система бронирования помещений ГБУ РС(Я) «Служба эксплуатационно-технического обеспечения».

## Быстрый запуск

### 1. Установка виртуального окружения

```bash
py -m venv venv
```

### 2. Активация виртуального окружения

```bash
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций (создание базы данных)

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Загрузка начальных данных (здания и помещения из xlsx)

```bash
python manage.py loaddata rental/fixtures/initial_data.json
```

### 6. Создание администратора

```bash
python manage.py createsuperuser
```

Введите логин, email и пароль. Этот пользователь получит доступ к панели `/admin/` и к разделу «Панель администратора» на сайте.

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Откройте в браузере: **http://127.0.0.1:8000/**

---

## Структура проекта

```
seto_project/
├── manage.py                      # Утилита командной строки Django
├── requirements.txt               # Зависимости Python
├── db.sqlite3                     # База данных (создаётся после migrate)
│
├── seto_project/                  # Настройки проекта
│   ├── settings.py                # Конфигурация Django (БД, приложения, ключ)
│   ├── urls.py                    # Главный маршрутизатор URL
│   └── wsgi.py                    # Точка входа для веб-сервера
│
└── rental/                        # Приложение бронирования
    ├── models.py                  # Модели БД: Building, Venue, Booking, EventLog
    ├── views.py                   # Обработчики HTTP-запросов
    ├── forms.py                   # HTML-формы и валидация
    ├── urls.py                    # URL-маршруты приложения
    ├── admin.py                   # Настройка административной панели
    ├── fixtures/
    │   └── initial_data.json      # Начальные данные (12 помещений из xlsx)
    └── templates/rental/
        ├── base.html              # Базовый шаблон (Bootstrap 5, навигация)
        ├── index.html             # Главная — список помещений с фильтрами
        ├── venue_detail.html      # Детальная страница помещения
        ├── book_venue.html        # Форма бронирования
        ├── my_bookings.html       # Список заявок пользователя
        ├── admin_bookings.html    # Панель управления заявками (admin)
        ├── login.html             # Страница входа
        └── register.html          # Страница регистрации
```

## Основные URL-адреса

| URL                       | Страница                           |
|---------------------------|------------------------------------|
| `/`                       | Список помещений                   |
| `/venue/<pk>/`            | Детальная страница помещения       |
| `/venue/<pk>/book/`       | Форма бронирования                 |
| `/my-bookings/`           | Мои заявки                         |
| `/admin-panel/`           | Панель администратора              |
| `/login/`                 | Вход                               |
| `/register/`              | Регистрация                        |
| `/admin/`                 | Django Admin (суперпользователь)   |

## Технический стек

- **Backend**: Python 3.x + Django 4.2
- **База данных**: SQLite (для разработки)
- **Frontend**: Django Template Language + Bootstrap 5 (CDN)
- **Аутентификация**: встроенная система Django (django.contrib.auth)

## Миграция на PostgreSQL (для продакшена)

В `settings.py` замените раздел DATABASES:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seto_db',
        'USER': 'seto_user',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Установите: `pip install psycopg2-binary`
