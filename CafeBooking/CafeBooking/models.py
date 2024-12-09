from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class Role(models.Model):
    name = models.CharField(null=False, max_length=20, verbose_name="Роль")

    def __str__(self) -> str:
        return self.decrypt()

    def crypt(self):
        name = self.name
        name = list(name)
        name[0], name[len(name) - 1] = name[len(name) - 1], name[0]
        self.name = "".join(name)

    def decrypt(self) -> str:
        name = self.name
        name = list(name)
        name[len(name) - 1], name[0] = name[0], name[len(name) - 1]
        return "".join(name)


class User(models.Model):
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=False, verbose_name="Роль"
    )
    name = models.CharField(max_length=20, null=False, verbose_name="Имя")
    lastname = models.CharField(max_length=20, null=False, verbose_name="Фамилия")
    email = models.EmailField(null=False, verbose_name="E-mail")
    login = models.CharField(max_length=20, null=False, verbose_name="Логин")
    password = models.CharField(max_length=255, null=False, verbose_name="Пароль")
    is_blocked = models.BooleanField(null=False, verbose_name="Заблокирован")

    def __str__(self) -> str:
        return f"{self.pk}:{self.name} {self.lastname}. Заблокирован: {self.get_is_blocked()}"

    def get_is_blocked(self):
        return "Да" if self.is_blocked else "Нет"


class Time(models.Model):
    time = models.CharField(max_length=15, null=False, verbose_name="Время")


class Status(models.Model):
    status = models.CharField(max_length=25, null=False, verbose_name="Статус")


class Office(models.Model):
    address = models.CharField(max_length=100, null=False, verbose_name="Адрес")

    def __str__(self) -> str:
        return f"{self.address}"


class Place(models.Model):
    short_name = models.CharField(
        max_length=5, null=False, verbose_name="Короткое название"
    )
    office = models.ForeignKey(
        Office, on_delete=models.CASCADE, null=False, verbose_name="Офис"
    )


class Type(models.Model):
    name = models.CharField(max_length=20, verbose_name="Тип")
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, null=False, verbose_name="Место"
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.place.short_name}, адрес: {self.place.office}"


class Reservation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, verbose_name="Пользователь"
    )
    time = models.ForeignKey(
        Time, on_delete=models.CASCADE, null=False, verbose_name="Время"
    )
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, null=False, verbose_name="Статус"
    )
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, null=False, verbose_name="Место"
    )
    date = models.DateField(null=False, verbose_name="Дата")
    cancel_reason = models.CharField(
        max_length=100, null=True, verbose_name="Причина отмены"
    )

    is_archivated = models.BooleanField(
        verbose_name="Архивированная запись", default=False, blank=False
    )
    creation_time = models.DateTimeField(auto_now_add=True)

    def check_continue(self):

        if self.time.time == "Утреннее":
            status = Status.objects.filter(status="Забронировано").first()
            if Reservation.objects.filter(
                time__time="Вечернее", date=self.date, status=status, type=self.type
            ).exists():
                return False
            return True
        else:
            return False


class Log(models.Model):
    timestamp = models.DateTimeField(verbose_name="Время лога", auto_now_add=True)
    action = models.CharField(verbose_name="Действие", max_length=255)

    def __str__(self) -> str:
        return f"{self.timestamp} : {self.action}"


class Setting(models.Model):
    months_to_archive = models.IntegerField(
        verbose_name="Срок хранения данных",
        default=2,
        validators=[MinValueValidator(1, "Нельзя поставить значение меньше 1")],
    )
