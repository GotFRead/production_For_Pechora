from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, User


# Create your models here.


class TypeOfWood(models.Model):
    name = models.CharField(max_length=50,
                            help_text='Введите тип древесины',
                            verbose_name='Наименование древесины')

    class Meta:
        verbose_name_plural = 'Породы'

    def __str__(self):
        return self.name


class SizeOfWood(models.Model):
    metric_of_wood = models.CharField(help_text='Укажите метрику',
                                      max_length=60,
                                      verbose_name='Диаметр древесины (от - до)')

    class Meta:
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return str(self.metric_of_wood)


class Deliveries(models.Model):
    count_deliveries = models.IntegerField(help_text='Введите количество',
                                           verbose_name='Количество бревен')

    cubage_deliveries = models.FloatField(help_text='Введите кубатуру поставки',
                                          verbose_name='Кубатура поставки')

    departure_point = models.CharField(max_length=100,
                                       help_text='Введите пункт отправления',
                                       verbose_name='Пункт отправление')

    arrival_point = models.CharField(max_length=100,
                                     help_text='Введите пункт прибытия',
                                     verbose_name='Пункт прибытия')

    date_arrival_point = models.DateField(help_text='Введите дату прибытия',
                                          verbose_name='Дата прибытия')

    truck_number = models.CharField(max_length=6 ,
                                    help_text='Введите номер машины',
                                    verbose_name='Номер машины')

    time_input_date = models.DateTimeField(auto_now=True,
                                           help_text='Введите время ввода данных',
                                           verbose_name='Время ввода данных')

    who_introduced = models.CharField(max_length=40,
                                      help_text='Введите ФИО',
                                      verbose_name='Кто ввел данные',
                                      default='test')

    bulk_deliveries = models.IntegerField(help_text='Введите количество',
                                          null=True,
                                          verbose_name='Количество не распределенных бревен')

    class Meta:
        verbose_name_plural = 'Поставки'

    def __str__(self):
        return str(self.id)


class Wood (models.Model):
    name_wood = models.ForeignKey('TypeOfWood', on_delete=models.CASCADE,
                                  help_text='Выберите наименование древесины',
                                  verbose_name='Наименование древесины', null=False)
    size_wood = models.ForeignKey('SizeOfWood', on_delete=models.CASCADE,
                                  help_text='Введите тип древесины',
                                  verbose_name='Класс древесины')
    count = models.IntegerField(help_text='Введите количество штук',
                                verbose_name='Количество штук')

    length = models.FloatField(help_text='Введите среднюю длину',
                               verbose_name='Средння длина')

    cubage = models.FloatField(help_text='Введите кубатуру',
                               verbose_name='Кубатура')

    delivery_number = models.ForeignKey('Deliveries', on_delete=models.CASCADE,
                                        help_text='Выберите номер поставки',
                                        verbose_name='Номер поставки')

    nature_size = models.FloatField(help_text='Введите размер',
                                    null=True,
                                    verbose_name='Точный размер группы')

    class Meta:
        verbose_name_plural = 'Древесина'

    def __str__(self):
        return str(self.name_wood)


class Expenses(models.Model):
    name_wood = models.ForeignKey('TypeOfWood',
                                  verbose_name='Наименование',
                                  on_delete=models.CASCADE,
                                  help_text='Выберите наименование древесины',
                                  null=False)
    size_wood = models.ForeignKey('SizeOfWood',
                                  verbose_name='Размер древесины',
                                  on_delete=models.CASCADE,
                                  help_text='Выберите класс древесины',
                                  null=False)
    count = models.IntegerField(help_text='Введите количество потраченных бревен',
                                verbose_name='Количество потраченных бревен')
    cubage = models.FloatField(help_text='Введите кубатуру',
                               verbose_name='Кубатура')
    length = models.FloatField(help_text='Введите среднюю длину',
                               verbose_name='Средння длина',
                               null=True)
    date_realization = models.DateField(auto_now=True, help_text='Введите дату реализации',
                                        verbose_name='Дата отправки на производство')

    class Meta:
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return str(self.name_wood)


class Balance(models.Model):
    name_wood = models.ForeignKey('TypeOfWood',
                                  verbose_name='Наименование',
                                  on_delete=models.CASCADE,
                                  help_text='Выберите наименование древесины',
                                  null=False)
    size_wood = models.ForeignKey('SizeOfWood',
                                  verbose_name='Размер древесины',
                                  on_delete=models.CASCADE,
                                  help_text='Выберите класс древесины',
                                  null=False)
    count = models.IntegerField(help_text='Введите количество оставшихся бревен',
                                     verbose_name='Количество оставшихся бревен')
    cubage = models.FloatField(help_text='Введите кубатуру',
                                 verbose_name='Кубатура')
    length = models.FloatField(help_text='Введите среднюю длину',
                               verbose_name='Средння длина',
                               null=True)

    class Meta:
        verbose_name_plural = 'Баланс'

    def __str__(self):
        return str(self.name_wood)

