# Generated by Django 4.0.6 on 2022-07-14 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_deliveries', models.IntegerField(help_text='Введите количество', verbose_name='Количество бревен')),
                ('cubage_deliveries', models.FloatField(help_text='Введите кубатуру поставки', verbose_name='Кубатура поставки')),
                ('departure_point', models.CharField(help_text='Введите пункт отправления', max_length=100, verbose_name='Пункт отправление')),
                ('arrival_point', models.CharField(help_text='Введите пункт прибытия', max_length=100, verbose_name='Пункт прибытия')),
                ('date_arrival_point', models.DateField(help_text='Введите дату прибытия', verbose_name='Дата прибытия')),
                ('truck_number', models.CharField(help_text='Введите номер машины', max_length=6, verbose_name='Номер машины')),
                ('time_input_date', models.DateTimeField(auto_now=True, help_text='Введите время ввода данных', verbose_name='Время ввода данных')),
                ('who_introduced', models.CharField(default='test', help_text='Введите ФИО', max_length=40, verbose_name='Кто ввел данные')),
                ('bulk_deliveries', models.IntegerField(help_text='Введите количество', null=True, verbose_name='Количество не распределенных бревен')),
            ],
        ),
        migrations.CreateModel(
            name='SizeOfWood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_of_wood', models.CharField(help_text='Укажите метрику', max_length=60, verbose_name='Диаметр древесины (от - до)')),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfWood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите тип древесины', max_length=50, verbose_name='Наименование древесины')),
            ],
        ),
        migrations.CreateModel(
            name='Wood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(help_text='Введите количество штук', verbose_name='Количество штук')),
                ('length', models.FloatField(help_text='Введите среднюю длину', verbose_name='Средння длина')),
                ('cubage', models.FloatField(help_text='Введите кубатуру', verbose_name='Кубатура')),
                ('nature_size', models.FloatField(help_text='Введите размер', null=True, verbose_name='Точный размер группы')),
                ('delivery_number', models.ForeignKey(help_text='Выберите номер поставки', on_delete=django.db.models.deletion.CASCADE, to='application.deliveries', verbose_name='Номер поставки')),
                ('name_wood', models.ForeignKey(help_text='Выберите наименование древесины', on_delete=django.db.models.deletion.CASCADE, to='application.typeofwood', verbose_name='Наименование древесины')),
                ('size_wood', models.ForeignKey(help_text='Введите тип древесины', on_delete=django.db.models.deletion.CASCADE, to='application.sizeofwood', verbose_name='Класс древесины')),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(help_text='Введите количество потраченных бревен', verbose_name='Количество потраченных бревен')),
                ('cubage', models.FloatField(help_text='Введите кубатуру', verbose_name='Кубатура')),
                ('length', models.FloatField(help_text='Введите среднюю длину', null=True, verbose_name='Средння длина')),
                ('date_realization', models.DateField(auto_now=True, help_text='Введите дату реализации', verbose_name='Дата отправки на производство')),
                ('name_wood', models.ForeignKey(help_text='Выберите наименование древесины', on_delete=django.db.models.deletion.CASCADE, to='application.typeofwood', verbose_name='Наименование')),
                ('size_wood', models.ForeignKey(help_text='Выберите класс древесины', on_delete=django.db.models.deletion.CASCADE, to='application.sizeofwood', verbose_name='Размер древесины')),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(help_text='Введите количество оставшихся бревен', verbose_name='Количество оставшихся бревен')),
                ('cubage', models.FloatField(help_text='Введите кубатуру', verbose_name='Кубатура')),
                ('length', models.FloatField(help_text='Введите среднюю длину', null=True, verbose_name='Средння длина')),
                ('name_wood', models.ForeignKey(help_text='Выберите наименование древесины', on_delete=django.db.models.deletion.CASCADE, to='application.typeofwood', verbose_name='Наименование')),
                ('size_wood', models.ForeignKey(help_text='Выберите класс древесины', on_delete=django.db.models.deletion.CASCADE, to='application.sizeofwood', verbose_name='Размер древесины')),
            ],
        ),
    ]