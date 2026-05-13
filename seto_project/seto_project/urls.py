"""
Главный маршрутизатор URL проекта.

urlpatterns — список маршрутов. Django проходит по нему сверху вниз
и направляет запрос в первый подходящий обработчик (view).

include() — подключает маршруты из другого файла urls.py (нашего приложения rental).
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # /admin/ — встроенная административная панель Django
    path('admin/', admin.site.urls),
    # '' — все остальные URL передаём в приложение rental
    path('', include('rental.urls')),
]
