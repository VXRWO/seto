"""
WSGI-интерфейс — точка входа для веб-серверов (Nginx, Apache, Gunicorn).
WSGI (Web Server Gateway Interface) — стандарт взаимодействия Python-приложения с сервером.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seto_project.settings')
application = get_wsgi_application()
