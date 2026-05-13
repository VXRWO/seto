"""
Регистрация моделей в административной панели Django (admin.py).

admin.site.register(Model, AdminClass) — подключает модель к панели /admin/.
ModelAdmin — класс для настройки отображения модели в панели.

list_display   — столбцы в списке объектов.
list_filter    — фильтры в правой панели.
search_fields  — поля для поиска через строку поиска.
ordering       — сортировка по умолчанию.
"""

from django.contrib import admin
from .models import Building, Venue, Booking, EventLog


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    """Настройка отображения зданий в панели администратора."""
    list_display = ('address', 'year_built', 'total_area', 'floors')
    search_fields = ('address',)
    ordering = ('address',)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """Настройка отображения помещений."""
    list_display = ('name', 'building', 'venue_type', 'floor', 'capacity', 'is_active', 'price_per_hour')
    list_filter = ('venue_type', 'is_active', 'building')
    search_fields = ('name', 'building__address')
    # list_editable — поля, которые можно редактировать прямо в списке (без входа в карточку)
    list_editable = ('is_active', 'price_per_hour')
    ordering = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Настройка отображения бронирований."""
    list_display = ('event_name', 'venue', 'user', 'start_datetime', 'end_datetime', 'status', 'is_priority')
    list_filter = ('status', 'is_priority', 'venue')
    search_fields = ('event_name', 'user__username', 'venue__name')
    # readonly_fields — поля только для чтения в форме редактирования
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    """Журнал событий — только для просмотра."""
    list_display = ('timestamp', 'event_type', 'user', 'description')
    list_filter = ('event_type',)
    search_fields = ('description', 'user__username')
    readonly_fields = ('timestamp', 'event_type', 'user', 'booking', 'description')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        """Запрещаем добавление записей вручную — журнал ведётся автоматически."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Запрещаем удаление записей журнала."""
        return False
