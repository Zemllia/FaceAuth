import datetime

from django.db import models
from django.utils.safestring import mark_safe


class Camera(models.Model):
    name = models.CharField(verbose_name='Название камеры', null=False, max_length=255)
    api_key = models.CharField(verbose_name="API ключ", null=False, max_length=32)
    need_access_level = models.ForeignKey("AccessLevel", on_delete=models.SET_NULL, related_name="cameras", null=True,
                                          verbose_name='Уровень доступа необходимый для взаимодействия')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"


class AccessLevel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название уровня доступа", null=False)
    level = models.IntegerField(verbose_name="Число уровня доступа(Доступ будет разрешен в том случае,"
                                             " если у человека это число уровеня доступа или выше)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Уровень доступа"
        verbose_name_plural = "Уровни доступа"


class Visitor(models.Model):
    first_name = models.CharField(max_length=255, null=False, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=False, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=255, null=False, verbose_name='Отчество')

    access_level = models.ForeignKey("AccessLevel", on_delete=models.SET_NULL, related_name="visitors", null=True,
                                     verbose_name='Уровень доступа пользователя')

    face_image = models.ImageField(verbose_name="Фотография лица", null=True, blank=True,
                                   upload_to='visitors_faces/')

    face_image_vectors = models.BinaryField(null=True)

    def __str__(self):
        return self.last_name + " " + self.first_name

    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Поситетели"


class CameraLog(models.Model):
    camera = models.ForeignKey("Camera", on_delete=models.CASCADE, related_name="logs", null=False,
                               verbose_name='Камера')
    success = models.BooleanField(verbose_name='Успешно?')
    image = models.ImageField(verbose_name='Изображение из запроса', null=False, blank=False,
                                  upload_to='log_faces/')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date.strftime("%H:%M %d.%m.%Y")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Логи"

