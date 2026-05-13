"""
Маршруты URL приложения rental (urls.py).

path('маршрут/', view_функция, name='имя') — регистрирует URL.
name='...' — именованный маршрут, используется в шаблонах через {% url 'имя' %}
  и в Python-коде через reverse('имя') или redirect('имя').

<int:pk> — конвертер типов: захватывает целое число из URL и передаёт в view как pk.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Главная страница — список помещений
    path('', views.index, name='index'),

    # Детальная страница помещения: /venue/5/
    path('venue/<int:pk>/', views.venue_detail, name='venue_detail'),

    # Форма бронирования: /venue/5/book/
    path('venue/<int:pk>/book/', views.book_venue, name='book_venue'),

    # Мои бронирования
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # Отмена бронирования: /booking/3/cancel/
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),

    # ── Администрирование ──────────────────────────────────────────
    path('admin-panel/', views.admin_bookings, name='admin_bookings'),
    path('booking/<int:pk>/update-status/', views.update_booking_status, name='update_booking_status'),

    # ── Аутентификация ─────────────────────────────────────────────
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
