#!/usr/bin/env python
"""
manage.py — утилита командной строки Django.

Основные команды:
  python manage.py runserver        — запуск сервера разработки
  python manage.py makemigrations   — создать файлы миграций по моделям
  python manage.py migrate          — применить миграции к БД
  python manage.py createsuperuser  — создать администратора
  python manage.py shell            — интерактивная консоль Django
"""
import os
import sys


def main():
    """Точка входа для всех команд Django."""
    # Указываем, какой файл настроек использовать
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seto_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django не установлен. Выполните: pip install django"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
