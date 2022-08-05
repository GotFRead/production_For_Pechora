import mimetypes
import numpy as numpy
import unicodecsv
from django.shortcuts import render
import os
import datetime
import re
import csv
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, HttpResponseNotModified, \
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseGone, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import *
from django.db import transaction
from django.contrib import messages
# Create your views here.


def m304():
    return HttpResponseNotModified()


def m400():
    return HttpResponseBadRequest("<h2>Запрос задан некорректно</h2>")


def m403():
    return HttpResponseForbidden( "<h2>Доступ к странице запрещен</h2>")


def m404():
    return HttpResponseNotFound("<h2>Данные по запросу отсутсвуют</h2>")


def m405():
    return HttpResponseNotAllowed("<h2>Доступ запрещен</h2>")


def m410():
    return HttpResponseGone("<h2>Данная страница удалена</h2>")


def m500():
    return HttpResponseServerError("<h2>Что-то пошло не так</h2>")


#def edit_delivery(request, id):
#    delivery = Deliveries.objects.get(id=id)
#
#    count_input = delivery.count_deliveries
#    count_input = delivery.count_deliveries
#
#    return render(request, 'edit_delivery.html',{'count_input': count_input,
#                                                 'lenght_input': lenght_input,
#                                                 'procent_input': procent_input,
#                                                 'number_input':number_input,
#                                                  'out_point_input': out_point_input,
#                                                 'input_point_input':input_point_input
#                                                 })

def check_role_users(verified_user):
    try:
        verified_user = User.objects.get(username=verified_user)
        if verified_user.is_staff is True or verified_user.is_superuser is True:
            return 'staff'
    except User.DoesNotExist:
        HttpResponseForbidden("<h2>Вы неавторизованы</h2>")


def expenses(request):
    if check_role_users(verified_user=request.user.username) == 'staff':
        try:
            type_of_logs = TypeOfWood.objects.all()
            class_of_log = SizeOfWood.objects.all()
            object_expenses = Expenses.objects.all()
            return render(request, 'Pechora/expenses.html', {'expenses': object_expenses,
                                                            'sidebarCategory': type_of_logs,
                                                            'subheadingCategory': class_of_log,
                                                            })
        except Expenses.DoesNotExist:
            error = 'Ошибка обработки баланса'
            return render(request, 'Pechora/balance.html', {'errors': error})

    else:
        return HttpResponseForbidden("<h2>Доступ к странице запрещен</h2>")


def main(request):
    # Вывод данных с фильтрацией
    typewood = request.GET.get('category', 1)
    classwood = request.GET.get('subcategory', 0)

    if typewood != 1 or classwood != 0:
        wood = Wood.objects.filter(name=f'{typewood}')
        type_of_logs = TypeOfWood.objects.filter(name=f'{typewood}')
        class_of_log = SizeOfWood.objects.filter(class_logs=classwood)

    else:
        wood = Wood.objects.all()
        type_of_logs = TypeOfWood.objects.all()
        class_of_log = SizeOfWood.objects.all()

    return render(request, 'Pechora/Main.html', {'logs': wood,
                                                 'typeOflogs': type_of_logs,
                                                 'sidebarCategory': type_of_logs,
                                                 'subheadingCategory': class_of_log})

    #return render(request, 'Pechora/Main.html')


def get_name_person(user_name):
    name = User.objects.get(username=user_name)
    return_name = f'{name.last_name} {name.first_name}'
    return return_name


def delivery(request):
    if check_role_users(verified_user=request.user.username) == 'staff':
        # Вывод данных с фильтрацией
        cubage = request.GET.get('category', 1)
        date = request.GET.get('subcategory', 0)

        if cubage != 1 or date != 0:
            deliveries = Deliveries.objects.filter(cubage_deliveries=cubage)
            cubage_deliveries = cubage
            date = Deliveries.objects.filter(date_arrival_point=date)

        else:
            obj_deliveries = Deliveries()
            deliveries = Deliveries.objects.all()
            date = Deliveries.date_arrival_point
            cubage_deliveries = obj_deliveries.cubage_deliveries
        return render(request, 'Pechora/delivery.html', {'deliveries': deliveries,
                                                         'sidebarCategory': date,
                                                         'subheadingCategory': cubage_deliveries
                                                         })
    else:
        return HttpResponseForbidden( "<h2>Доступ к странице запрещен</h2>")


def register(request):
    if request.method == 'POST':
        user_form = RigistrForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(user_form.cleaned_data['password'])

            new_user.save()

            return render(request, 'Author.html')

    else:
        user_form = RigistrForm()
    return render(request, 'Pechora/Registration.html', {'user_form': user_form})


def type(request):
    if check_role_users(verified_user=request.user.username) == 'staff':
        types = TypeOfWood.objects.all()
        return render(request, 'Pechora/typeofwood.html', {'type': types})
    else:
        return HttpResponseForbidden( "<h2>Доступ к странице запрещен</h2>")


@transaction.atomic
def create_delivery(request):
    try:
        if request.method == 'POST':
            object_delivery = Deliveries()
            object_delivery.count_deliveries = int(request.POST.get('count'))
            object_delivery.bulk_deliveries = int(request.POST.get('count'))
            object_delivery.date_arrival_point = datetime.date.today()
            object_delivery.departure_point = request.POST.get('out_point')
            object_delivery.arrival_point = request.POST.get('input_point')
            truck_number = request.POST.get('number')

            object_delivery.truck_number = truck_number

            procent = int(request.POST.get('procent'))
            lenght = float(request.POST.get('lenght'))

            object_delivery.cubage_deliveries = lenght*procent*object_delivery.count_deliveries/100
            object_delivery.time_input_date = datetime.datetime.now()
            object_delivery.who_introduced = get_name_person(request.user.username)

            if procent >= 100 or procent < 0:
                errors = 'Ошибка ввода: Процент заполнения указан неверно'
                messages.error(request, f'{errors}')
                return HttpResponseRedirect('/create_delivery/')

            match = re.fullmatch(r'\w\d{3}\w{2}', truck_number)
            if not match:
                errors = 'Ошибка ввода: Номер введен некорректно'
                messages.error(request, f'{errors}')
                return HttpResponseRedirect('/create_delivery/')

            object_delivery.save()
            name_person = get_name_person(request.user.username)
            deliveries = Deliveries.objects.filter(who_introduced=name_person)
            successful = 'Успешно'
            messages.success(request, f'{successful}')
            return HttpResponseRedirect('/create_delivery/')

        name_person = get_name_person(request.user.username)
        deliveries = Deliveries.objects.filter(who_introduced=name_person)
        return render(request, 'Pechora/input_delivery.html', {'deliveries': deliveries})

    except Deliveries.DoesNotExist:
        return HttpResponseNotFound("<h2>Deliveries not found</h2>")

    except ValueError:
        errors = 'Ошибка ввода: Поля заполнены неверно'
        messages.error(request, f'{errors}')
        return HttpResponseRedirect('/create_delivery/')


def get_id_size(diametr: int) -> id:
    if diametr < 10:
        return 1
    elif diametr < 21:
        return 2
    elif diametr < 23:
        return 3
    elif diametr < 25:
        return 4
    elif diametr < 27:
        return 5
    elif diametr < 29:
        return 6
    elif diametr < 31:
        return 7
    elif diametr < 33:
        return 8
    elif diametr < 35:
        return 9
    elif diametr < 60:
        return 10
    else:
        return 10


#def add_wood_control(request, errors='', msg=''):
#    if errors == '' and msg == '':
#        return add_wood(request)
#    elif msg == '':
#        return add_wood(request, errors = errors)
#    else:
#        return add_wood(request, msg = msg)


@transaction.atomic
def add_wood(request):
    try:
        if request.method == 'POST':
            object_wood = Wood()

            object_wood.count = int(request.POST.get('count'))
            object_wood.length = request.POST.get('lenght')

            name_wood = int(request.POST.get('name_wood'))
            object_wood.name_wood = TypeOfWood.objects.get(id=name_wood)

            object_wood.count = int(request.POST.get('count'))
            object_wood.length = request.POST.get('lenght')

            id_delivery = int(request.POST.get('id_delivery'))
            object_wood.delivery_number = Deliveries.objects.get(id=id_delivery)

            size = int(request.POST.get('diametr'))

            object_wood.nature_size = size

            id_size = get_id_size(size)

            object_wood.size_wood = SizeOfWood.objects.get(id=id_size)

            object_wood.cubage = (int(object_wood.length) * ((size/2) ** 2) * int(object_wood.count)) / 100

            object_delivery = Deliveries.objects.get(id=id_delivery)

            if object_wood.count <= object_delivery.bulk_deliveries:
                object_delivery.bulk_deliveries = object_delivery.bulk_deliveries - object_wood.count
                object_delivery.save()
            else:
                errors = 'Ошибка ввода: Количество бревен указано неверно'
                messages.error(request, f'{errors}')
                return HttpResponseRedirect('/add_wood/')

            name_wood = TypeOfWood.objects.get(id=name_wood)
            size_woods = SizeOfWood.objects.get(id=id_size)

            balance = Balance.objects.filter(name_wood=name_wood,
                                             size_wood=size_woods,
                                             length=object_wood.length)

            if balance.count() > 0:
                add_balance = Balance.objects.get(name_wood=name_wood,
                                                  size_wood=size_woods,
                                                  length=object_wood.length)
                add_balance.count = add_balance.count + int(object_wood.count)

                add_balance.cubage = add_balance.cubage + object_wood.cubage

                add_balance.save()

            else:
                new_balance = Balance(name_wood=name_wood,
                                      size_wood=size_woods,
                                      length=object_wood.length,
                                      count=int(object_wood.count),
                                      cubage=(int(object_wood.length) * ((size/2) ** 2) * int(object_wood.count)) / 100)
                new_balance.save()

            object_wood.save()
            successful = 'Успешно'
            messages.success(request, f'{successful}')
            return HttpResponseRedirect('/add_wood/')

            #return render(request, 'Pechora/input_wood.html', {'success': successful})

            #return render(request, 'Pechora/input_wood.html', {'success': successful})

        else:
            type_of_wood = TypeOfWood.objects.all()
            size_of_wood = SizeOfWood.objects.all()
            deliveries = Deliveries.objects.all()
            return render(request, 'Pechora/input_wood.html', {'type_of_woods': type_of_wood,
                                                               'size_of_woods': size_of_wood,
                                                               'deliveries': deliveries})
    except Wood.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

    except Balance.DoesNotExist:
        new_balance = Balance(name_wood=name_wood,
                              size_wood=size,
                              length=object_wood.length)
        new_balance.save()
        successful = 'Успешно'
        messages.success(request, f'{successful}')
        return HttpResponseRedirect('/add_wood/')


@transaction.atomic
def add_expenses(request):
    try:
        if request.method == 'POST':
            object_expenses = Expenses()

            name_wood = int(request.POST.get('name_wood'))
            object_expenses.name_wood = TypeOfWood.objects.get(id=name_wood)

            size = int(request.POST.get('diametr'))

            id_size = get_id_size(size)

            object_expenses.size_wood = SizeOfWood.objects.get(id=id_size)
            size_wood = SizeOfWood.objects.get(id=id_size)

            object_expenses.length = request.POST.get('length')
            length = float(request.POST.get('length'))

            object_expenses.count = int(request.POST.get('count'))
            count = int(request.POST.get('count'))
            object_expenses.date_realization = datetime.datetime.now()

            object_expenses.cubage = (count * ((size/2) ** 2) * length)/100

            object_balance = Balance.objects.filter(name_wood=name_wood,
                                              length=length,
                                              size_wood=size_wood)

            count_balance = object_balance[0].count

            if object_balance.count() == 0:
                errors = 'Ошибка ввода: Древесина по заданным параметрам отсутствует'
                messages.error(request, f'{errors}')
                return HttpResponseRedirect('/add_expenses/')
            elif object_expenses.count <= count_balance:

                if count_balance < 0:
                    errors = 'Ошибка ввода: Списание данной древесины невозможно'
                    messages.error(request, f'{errors}')
                    return HttpResponseRedirect('/add_expenses/')

                else:
                    decrease_balance = Balance.objects.get(name_wood=name_wood,
                                                           size_wood=size_wood,
                                                           length=object_expenses.length)

                    if decrease_balance.count - int(object_expenses.count) < 0:
                        raise TypeError
                    else:
                        decrease_balance.count = decrease_balance.count - int(object_expenses.count)

                        decrease_balance.cubage = decrease_balance.cubage - object_expenses.cubage

                        decrease_balance.save()

            else:
                errors = 'Ошибка ввода: Количество бревен указано неверно'
                messages.error(request, f'{errors}')
                return HttpResponseRedirect('/add_expenses/')

            object_expenses.save()
            successful = 'Успешно'
            messages.success(request, f'{successful}')
            return HttpResponseRedirect('/add_expenses/')
        else:
            type_of_wood = TypeOfWood.objects.all()
            size_of_wood = SizeOfWood.objects.all()
            return render(request, 'Pechora/input_expenses.html', {'type_of_woods': type_of_wood,
                                                                   'size_of_woods': size_of_wood})

    except IndexError:
        errors = 'Ошибка ввода: Какой-то из параметров указан неверно'
        messages.error(request, f'{errors}')
        return HttpResponseRedirect('/add_expenses/')
    except TypeError:
        errors = 'Ошибка ввода: Количество бревен превышает запас'
        messages.error(request, f'{errors}')
        return HttpResponseRedirect('/add_expenses/')

    except Expenses.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")

    except SizeOfWood.DoesNotExist:
        errors = 'Ошибка ввода: Древесина заданного размера отсутствует'
        messages.error(request, f'{errors}')
        return HttpResponseRedirect('/add_expenses/')

    except Wood.DoesNotExist:
        errors = 'Ошибка ввода: Древесина по заданным параметрам отсутствует'
        messages.error(request, f'{errors}')
        return HttpResponseRedirect('/add_expenses/')


@transaction.atomic
def balance(request):
    if check_role_users(verified_user=request.user.username) == 'staff':
        try:
            type_of_logs = TypeOfWood.objects.all()
            class_of_log = SizeOfWood.objects.all()
            object_balance = Balance.objects.all()
            return render(request, 'Pechora/balance.html', {'balances': object_balance,
                                                            'sidebarCategory': type_of_logs,
                                                            'subheadingCategory': class_of_log,
                                                            })

        except Balance.DoesNotExist:
            error = 'Ошибка обработки баланса'
            messages.error(request, f'{error}')
            return HttpResponseRedirect('/balance/')

    else:
        return HttpResponseForbidden("<h2>Доступ к странице запрещен</h2>")


def create_report_delivery(request):
    if check_role_users(verified_user=request.user.username) == 'staff':

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="report {datetime.date.today()}.csv"'},
        )

        fieldnames = ['Кол-во деревесины', 'Кубатура', 'Место отправки',
                      'Место приемки', 'Дата приемки', 'Номер машины',
                      'Время приемки', 'Кто принял', 'Неотсортированно']

        writer = unicodecsv.writer(response, encoding='ANSI')

        writer.writerow(['Поставки'])

        writer.writerow(fieldnames)

        array_input = ['1', '1', '1', '1', '1', '1', '1', '1', '1']

        #for delivery in Deliveries.objects.filter(date_arrival_point=datetime.date.today()):
        for delivery in Deliveries.objects.all():
            array_input[0] = delivery.count_deliveries
            array_input[1] = delivery.cubage_deliveries
            array_input[2] = delivery.departure_point
            array_input[3] = delivery.arrival_point
            array_input[4] = delivery.date_arrival_point
            array_input[5] = delivery.truck_number
            array_input[6] = delivery.time_input_date
            array_input[7] = delivery.who_introduced
            array_input[8] = delivery.bulk_deliveries
            writer.writerow(array_input)
        return response
    else:
        return HttpResponseForbidden("<h2>Доступ к странице запрещен</h2>")


def create_report_expenses(request):
    if check_role_users(verified_user=request.user.username) == 'staff':
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="report {datetime.date.today()}.csv"'},
        )

        fieldnames = ['Кол-во деревесины', 'Кубатура', 'Место отправки',
                      'Место приемки', 'Дата принтяиия', 'Дата реализации']

        writer = unicodecsv.writer(response, encoding='ANSI')

        writer.writerow(['Расходы'])

        writer.writerow(fieldnames)

        array_input = ['1', '1', '1', '1', '1', '1']

        for expenses in Expenses.objects.all():
            object_name_wood = str(expenses.name_wood)
            object_size_wood = str(expenses.size_wood)
            array_input[0] = object_name_wood
            array_input[1] = object_size_wood
            array_input[2] = expenses.count
            array_input[3] = expenses.cubage
            array_input[4] = expenses.length
            array_input[5] = expenses.date_realization
            writer.writerow(array_input)
        return response
    else:
        return HttpResponseForbidden("<h2>Доступ к странице запрещен</h2>")


def create_report_balance(request):
    if check_role_users(verified_user=request.user.username) == 'staff':
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="report {datetime.date.today()}.csv"'},
        )

        fieldnames = ['Порода деревесины', 'Размер', 'Кол-во',
                      'Кубатура', 'Длина']

        writer = unicodecsv.writer(response, encoding='ANSI')

        writer.writerow(['Баланс'])

        writer.writerow(fieldnames)

        array_input = ['1', '1', '1', '1', '1']

        for balances in Balance.objects.all():
            object_name_wood = str(balances.name_wood)
            object_size_wood = str(balances.size_wood)
            array_input[0] = object_name_wood
            array_input[1] = object_size_wood
            array_input[2] = balances.count
            array_input[3] = balances.cubage
            array_input[4] = balances.length
            writer.writerow(array_input)
        return response

    else:
        return HttpResponseForbidden("<h2>Доступ к странице запрещен</h2>")


def create_report_type_of_wood(request):
    if check_role_users(verified_user=request.user.username) == 'staff':
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="report {datetime.date.today()}.csv"'},
        )

        fieldnames = ['Индекс древесины', 'Наименование']

        writer = unicodecsv.writer(response, encoding='ANSI')

        writer.writerow(['Номенклатура древесины'])

        writer.writerow(fieldnames)

        array_input = ['1', '1']

        # for delivery in Deliveries.objects.filter(date_arrival_point=datetime.date.today()):
        for type in TypeOfWood.objects.all():
            array_input[0] = type.id
            array_input[1] = type.name
            writer.writerow(array_input)
        return response
    else:
        return HttpResponseForbidden("<h2>Доступ к странице запрещен</h2>")


class Registration(CreateView):
    form_class = RigistrForm
    template_name = 'Pechora/Registration.html'
    success_url = reverse_lazy('login')


class Registr(CreateView):
    form_class = Registr
    template_name = 'Pechora/registr.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'Author.html'

