"""
Django настройки для проекта СЭТО.

SECRET_KEY — секретный ключ для криптографии (подписи сессий, токенов).
DEBUG=True — режим отладки: показывает подробные ошибки. В продакшене ставим False.
INSTALLED_APPS — список всех подключённых приложений Django.
DATABASES — подключение к базе данных. Используем SQLite для простоты.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ВАЖНО: в продакшене заменить на случайный длинный ключ и хранить в переменных окружения
SECRET_KEY = 'django-insecure-seto-rental-project-2026-yakutsk-secret-key'

# Режим отладки — True только при разработке
DEBUG = True

ALLOWED_HOSTS = ['*']

# Список приложений: стандартные Django + наше приложение rental
INSTALLED_APPS = [
    'django.contrib.admin',        # Административная панель
    'django.contrib.auth',         # Система аутентификации
    'django.contrib.contenttypes', # Типы контента (нужен для прав доступа)
    'django.contrib.sessions',     # Сессии пользователей
    'django.contrib.messages',     # Flash-сообщения
    'django.contrib.staticfiles',  # Статические файлы (CSS, JS)
    'rental',                      # Наше приложение бронирования
]

# Промежуточные слои (middleware) — обрабатывают каждый запрос/ответ по цепочке
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',       # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'seto_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Автоматически ищет шаблоны в папке templates/ каждого приложения
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'seto_project.wsgi.application'

# База данных: SQLite — файловая БД, идеально для разработки и небольших проектов.
# Для продакшена заменить на PostgreSQL (см. документацию Django).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Движок БД
        'NAME': BASE_DIR / 'db.sqlite3',          # Файл базы данных в корне проекта
    }
}

# Валидаторы паролей — требования к сложности пароля пользователей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'    # Язык интерфейса
TIME_ZONE = 'Asia/Yakutsk' # Часовой пояс Якутска
USE_I18N = True
USE_TZ = True

# URL и директория для статических файлов (CSS, JS, изображения)
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# После входа/выхода перенаправлять на главную страницу
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
