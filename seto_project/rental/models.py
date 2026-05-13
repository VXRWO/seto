"""
Модели данных (models.py) — описание таблиц базы данных через Python-классы.

Django ORM (Object-Relational Mapping) автоматически создаёт SQL-таблицы
на основе этих классов. Каждый атрибут класса = столбец в таблице БД.

Команды для применения моделей к БД:
  python manage.py makemigrations  — создаёт файлы миграций (инструкции для БД)
  python manage.py migrate         — применяет миграции, создаёт/изменяет таблицы
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Building(models.Model):
    """
    Модель здания — хранит информацию о зданиях ГБУ РС(Я) СЭТО.
    Данные взяты из файла Данные_по_зданиям.xlsx.
    
    models.CharField  — текстовое поле с ограничением длины (VARCHAR в SQL)
    models.FloatField — поле с плавающей точкой (REAL в SQL)
    models.IntegerField — целочисленное поле (INTEGER в SQL)
    """
    address = models.CharField(max_length=255, verbose_name='Адрес')
    year_built = models.CharField(max_length=50, blank=True, verbose_name='Год постройки')
    # blank=True, null=True — поле необязательное (можно оставить пустым)
    total_area = models.FloatField(blank=True, null=True, verbose_name='Площадь, м²')
    floors = models.IntegerField(blank=True, null=True, verbose_name='Этажность')
    note = models.TextField(blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'
        ordering = ['address']  # Сортировка по умолчанию

    def __str__(self):
        # Метод __str__ определяет строковое представление объекта
        return self.address


class Venue(models.Model):
    """
    Модель помещения/площадки — основная сущность для бронирования.
    Соответствует «паспорту помещения» из Положения СЭТО (пункт 2.2).
    
    ForeignKey — внешний ключ, связывает помещение со зданием (отношение многие-к-одному).
    on_delete=models.SET_NULL — при удалении здания, поле building станет NULL (не удалять помещение).
    """

    VENUE_TYPES = [
        ('hall', 'Актовый зал'),
        ('conference', 'Конференц-зал'),
        ('sport', 'Спортивный зал'),
        ('rest', 'Комната отдыха'),
        ('other', 'Иное помещение'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название помещения')
    # ForeignKey — связь с моделью Building: у одного здания может быть много помещений
    building = models.ForeignKey(
        Building,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='venues',  # building.venues.all() — все помещения здания
        verbose_name='Здание'
    )
    venue_type = models.CharField(
        max_length=20, choices=VENUE_TYPES,
        default='hall', verbose_name='Тип помещения'
    )
    floor = models.IntegerField(blank=True, null=True, verbose_name='Этаж')
    area = models.FloatField(blank=True, null=True, verbose_name='Площадь, м²')
    capacity = models.IntegerField(verbose_name='Вместимость (чел.)')
    equipment = models.TextField(blank=True, verbose_name='Оборудование')
    special_conditions = models.TextField(blank=True, verbose_name='Особые условия')
    # BooleanField — логическое поле True/False (BOOLEAN в SQL)
    is_active = models.BooleanField(default=True, verbose_name='Доступно для бронирования')
    work_start = models.TimeField(default='08:00', verbose_name='Начало работы')
    work_end = models.TimeField(default='20:00', verbose_name='Конец работы')
    price_per_hour = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='Цена за час (руб.)'
    )
    image_url = models.CharField(max_length=500, blank=True, verbose_name='Фото (URL)')

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} — {self.building}'

    def get_type_display_ru(self):
        return dict(self.VENUE_TYPES).get(self.venue_type, '')


class Booking(models.Model):
    """
    Модель бронирования — центральная сущность системы.
    Связывает пользователя с помещением на конкретный временной интервал.
    
    DateTimeField — поле даты и времени (DATETIME в SQL).
    auto_now_add=True — автоматически записывает дату/время создания записи.
    """

    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('rejected', 'Отклонено'),
        ('completed', 'Завершено'),
    ]

    # ForeignKey на встроенную модель User из django.contrib.auth
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # При удалении пользователя удалить его бронирования
        related_name='bookings',
        verbose_name='Пользователь'
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Помещение'
    )
    event_name = models.CharField(max_length=255, verbose_name='Название мероприятия')
    start_datetime = models.DateTimeField(verbose_name='Начало')
    end_datetime = models.DateTimeField(verbose_name='Окончание')
    participants_count = models.IntegerField(verbose_name='Количество участников')
    equipment_needed = models.TextField(blank=True, verbose_name='Необходимое оборудование')
    special_requirements = models.TextField(blank=True, verbose_name='Особые требования')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name='Статус'
    )
    is_priority = models.BooleanField(default=False, verbose_name='Приоритетное бронирование')
    admin_comment = models.TextField(blank=True, verbose_name='Комментарий администратора')
    # auto_now_add — автоматически устанавливается при создании объекта
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # auto_now — обновляется при каждом сохранении объекта
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.event_name} | {self.venue} | {self.start_datetime:%d.%m.%Y %H:%M}'

    def clean(self):
        """
        Валидация модели — вызывается перед сохранением.
        Проверяет корректность дат и отсутствие конфликтов бронирования.
        
        ValidationError — исключение Django, которое показывает ошибку пользователю.
        """
        if self.start_datetime and self.end_datetime:
            if self.end_datetime <= self.start_datetime:
                raise ValidationError('Время окончания должно быть позже времени начала.')

            # Проверка пересечений: ищем подтверждённые брони того же помещения
            # в пересекающийся временной интервал (исключая текущую запись при редактировании)
            overlapping = Booking.objects.filter(
                venue=self.venue,
                status='confirmed',
                start_datetime__lt=self.end_datetime,  # __lt = "меньше чем" (Less Than)
                end_datetime__gt=self.start_datetime,  # __gt = "больше чем" (Greater Than)
            )
            # exclude(pk=self.pk) — исключаем себя (при редактировании)
            if self.pk:
                overlapping = overlapping.exclude(pk=self.pk)
            if overlapping.exists():
                raise ValidationError(
                    'Помещение уже забронировано на этот временной интервал.'
                )

    def duration_hours(self):
        """Длительность бронирования в часах."""
        delta = self.end_datetime - self.start_datetime
        return round(delta.total_seconds() / 3600, 1)

    def total_cost(self):
        """Итоговая стоимость аренды."""
        return round(float(self.venue.price_per_hour) * self.duration_hours(), 2)


class EventLog(models.Model):
    """
    Журнал событий — фиксирует все действия в системе.
    Соответствует требованию раздела 5 Положения об ответственности.
    
    TextField — текстовое поле без ограничения длины (TEXT в SQL).
    """

    EVENT_TYPES = [
        ('booking_created', 'Создание бронирования'),
        ('booking_confirmed', 'Подтверждение бронирования'),
        ('booking_cancelled', 'Отмена бронирования'),
        ('booking_rejected', 'Отклонение бронирования'),
        ('user_login', 'Вход пользователя'),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, verbose_name='Тип события')
    # null=True — разрешает NULL в БД; blank=True — разрешает пустое значение в формах
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Пользователь'
    )
    booking = models.ForeignKey(
        Booking, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Бронирование'
    )
    description = models.TextField(verbose_name='Описание')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время события')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'Журнал событий'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.timestamp:%d.%m.%Y %H:%M} — {self.get_event_type_display()}'
