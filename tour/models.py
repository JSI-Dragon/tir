from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

User = get_user_model()


class Banner(models.Model):
    title = models.CharField('Название', max_length=100)
    banner_image = models.ImageField('Изображение', upload_to='banners/')
    is_asset = models.BooleanField('Активность', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'


class Category(models.Model):
    title = models.CharField('Название категории', max_length=100)
    description = models.TextField('Описание категории')
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class RegionTour(models.Model):
    title = models.CharField('Название региона', max_length=100)
    description = models.TextField('Описание региона')
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Убедитесь, что это поле существует
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class DateTour(models.Model):
    start_date = models.DateField('Дата начала тура')
    end_date = models.DateField('Дата окончания тура')

    TOUR_TYPES = [
        ('group', 'Групповой'),
        ('individual', 'Индивидуальный'),
    ]
    tour_type = models.CharField('Тип тура', max_length=20, choices=TOUR_TYPES)

    SEASON_CHOICES = [
        ('spring', 'Весна'),
        ('summer', 'Лето'),
        ('autumn', 'Осень'),
        ('winter', 'Зима'),
    ]
    season = models.CharField('Сезон', max_length=100, choices=SEASON_CHOICES)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError('Дата окончания тура не может быть раньше даты начала.')

    def __str__(self):
        return f"{self.start_date} - {self.end_date} ({self.get_season_display()})"


class Tour(models.Model):
    author = models.CharField('Автор', max_length=100)
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание тура', max_length=500)
    category = models.ManyToManyField(Category, related_name='tours')
    date_tour = models.ManyToManyField(DateTour, related_name='tours')
    route_tour = models.CharField('Маршрут тура', max_length=200)
    duration = models.IntegerField('Продолжительность (дни)')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    region = models.ManyToManyField(RegionTour, related_name='tours')
    discount_price = models.DecimalField('Цена со скидкой', max_digits=10, decimal_places=2, blank=True, null=True)
    discount_start_date = models.DateTimeField('Дата начала скидки', blank=True, null=True)
    discount_end_date = models.DateTimeField('Дата окончания скидки', blank=True, null=True)
    participants_price = models.DecimalField('Цена за участника', max_digits=10, decimal_places=2)
    max_participants = models.IntegerField('Максимальное количество участников', validators=[MinValueValidator(1)])
    images = models.ManyToManyField('TourImage', related_name='tours', blank=True)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_date = models.DateTimeField('Дата обновления', auto_now=True)
    is_published = models.BooleanField('Опубликован', default=False)
    is_admin = models.BooleanField('Админская', default=False)

    def __str__(self):
        return self.title


class TourImage(models.Model):
    image = models.ImageField('Изображение', upload_to='tours_images/')

    def __str__(self):
        return f"Image {self.id}"


class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookings')
    date = models.ForeignKey(DateTour, on_delete=models.CASCADE, related_name='bookings')
    participants = models.IntegerField('Количество участников', validators=[MinValueValidator(1)])
    total_price = models.DecimalField('Итоговая цена', max_digits=10, decimal_places=2)

    STATUS_CHOICES = [
        (1, 'В ожидании'),
        (2, 'Подтверждено'),
        (3, 'Отклонено'),
    ]
    status = models.PositiveSmallIntegerField('Статус бронирования', choices=STATUS_CHOICES)

    def __str__(self):
        return f"Booking {self.id} for {self.tour.title or 'Untitled Tour'}"


class Rating(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_date = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['tour', 'user']),
        ]

    def __str__(self):
        return f"Rating {self.id} for {self.tour.title}"


class Feedback(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)

    def __str__(self):
        full_path = [self.comment]
        k = self.parent
        while k is not None:
            full_path.append(k.comment)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class FavoriteList(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tour', 'user')
