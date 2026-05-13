from django.apps import AppConfig


class RentalConfig(AppConfig):
    """
    Конфигурация приложения rental.
    AppConfig — класс для настройки Django-приложения.
    default_auto_field — тип поля для автоматически создаваемых первичных ключей (id).
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rental'
    verbose_name = 'Аренда помещений'
