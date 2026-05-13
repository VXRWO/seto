
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Building, Venue, Booking, EventLog
from .forms import BookingForm, LoginForm, RegisterForm


def index(request):
    """
    Главная страница — показывает список доступных помещений.

    Venue.objects.filter(is_active=True) — ORM-запрос к БД:
    SELECT * FROM rental_venue WHERE is_active = 1
    """
    venues = Venue.objects.filter(is_active=True).select_related('building')
    # select_related('building') — JOIN с таблицей Building за один SQL-запрос (оптимизация)

    venue_type = request.GET.get('type')       # Параметр из URL: ?type=hall
    capacity = request.GET.get('capacity')     # Параметр из URL: ?capacity=50
    search = request.GET.get('search', '')     # Параметр поиска: ?search=...

    if venue_type:
        venues = venues.filter(venue_type=venue_type)
    if capacity:
        # __gte = "больше или равно" (Greater Than or Equal)
        venues = venues.filter(capacity__gte=int(capacity))
    if search:
        # Q-объекты позволяют строить сложные условия OR / AND
        venues = venues.filter(
            Q(name__icontains=search) |           # icontains — регистронезависимый поиск
            Q(building__address__icontains=search)
        )

    # context — словарь данных, передаваемых в шаблон
    context = {
        'venues': venues,
        'venue_types': Venue.VENUE_TYPES,
        'selected_type': venue_type,
        'search': search,
    }
    return render(request, 'rental/index.html', context)


def venue_detail(request, pk):
    """
    Детальная страница помещения.

    get_object_or_404 — получает объект по pk; если не найден — возвращает HTTP 404.
    pk — Primary Key, уникальный идентификатор записи в БД.
    """
    venue = get_object_or_404(Venue, pk=pk)
    # Получаем подтверждённые будущие бронирования этого помещения
    bookings = venue.bookings.filter(
        status='confirmed',
        end_datetime__gte=timezone.now()  # __gte = >= текущего времени
    ).order_by('start_datetime')

    context = {'venue': venue, 'bookings': bookings}
    return render(request, 'rental/venue_detail.html', context)


@login_required  # Декоратор: если не авторизован — перенаправляет на LOGIN_URL
def book_venue(request, pk):
    """
    Страница создания бронирования.

    request.method == 'POST' — проверяем, была ли отправлена форма.
    form.is_valid() — запускает валидацию всех полей формы.
    form.save(commit=False) — создаёт объект, но НЕ сохраняет в БД (нам нужно добавить user).
    """
    venue = get_object_or_404(Venue, pk=pk, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)

        # создаём объект ДО валидации
        form.instance.user = request.user
        form.instance.venue = venue

        if form.is_valid():
            booking = form.save(commit=False)

            try:
                booking.full_clean()  # проверка пересечений
                booking.save()

                EventLog.objects.create(
                    event_type='booking_created',
                    user=request.user,
                    booking=booking,
                    description=f'Создано бронирование: {booking.event_name} в {venue.name}'
                )

                messages.success(request, 'Заявка на бронирование успешно отправлена!')
                return redirect('my_bookings')

            except Exception as e:
                messages.error(request, f'Ошибка: {e}')

    else:
        form = BookingForm()

    return render(request, 'rental/book_venue.html', {'form': form, 'venue': venue})


@login_required
def my_bookings(request):
    """Список бронирований текущего пользователя."""
    # request.user.bookings — обратная связь через related_name='bookings'
    bookings = request.user.bookings.all().select_related('venue', 'venue__building')
    return render(request, 'rental/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    """Отмена бронирования пользователем."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status in ('pending', 'confirmed'):
        booking.status = 'cancelled'
        booking.save()
        EventLog.objects.create(
            event_type='booking_cancelled',
            user=request.user,
            booking=booking,
            description=f'Пользователь отменил бронирование: {booking.event_name}'
        )
        messages.success(request, 'Бронирование отменено.')
    return redirect('my_bookings')


# ── Административные представления ─────────────────────────────────────────

@login_required
def admin_bookings(request):
    """
    Панель администратора — список всех бронирований.
    is_staff — встроенный флаг Django для сотрудников (администраторов).
    """
    if not request.user.is_staff:
        messages.error(request, 'Доступ запрещён.')
        return redirect('index')

    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.all().select_related('user', 'venue', 'venue__building')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    context = {
        'bookings': bookings,
        'status_choices': Booking.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'rental/admin_bookings.html', context)


@login_required
def update_booking_status(request, pk):
    """Изменение статуса бронирования администратором."""
    if not request.user.is_staff:
        return redirect('index')

    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        comment = request.POST.get('admin_comment', '')
        if new_status in dict(Booking.STATUS_CHOICES):
            old_status = booking.get_status_display()
            booking.status = new_status
            booking.admin_comment = comment
            booking.save()
            EventLog.objects.create(
                event_type=f'booking_{new_status}',
                user=request.user,
                booking=booking,
                description=f'Статус изменён с «{old_status}» на «{booking.get_status_display()}». Комментарий: {comment}'
            )
            messages.success(request, 'Статус обновлён.')
    return redirect('admin_bookings')


# ── Аутентификация ──────────────────────────────────────────────────────────

def login_view(request):
    """
    Страница входа в систему.
    authenticate() — проверяет логин и пароль, возвращает объект User или None.
    login() — создаёт сессию для пользователя (записывает в куки session_id).
    """
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()
    return render(request, 'rental/login.html', {'form': form})


def register_view(request):
    """Страница регистрации нового пользователя."""
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()        # Создаём пользователя в БД
            login(request, user)      # Автоматически входим после регистрации
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'rental/register.html', {'form': form})


def logout_view(request):
    """Выход из системы — удаляет сессию пользователя."""
    logout(request)
    return redirect('index')
