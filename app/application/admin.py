from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(SizeOfWood)
class ClassOfLogsAdmin(admin.ModelAdmin):
    list_display = ('metric_of_wood',)
    list_filter = ('metric_of_wood',)


@admin.register(Deliveries)
class DeliveriesAdmin(admin.ModelAdmin):
    list_display = ('date_arrival_point', 'cubage_deliveries', 'arrival_point',
                    'count_deliveries', 'truck_number', 'time_input_date',
                    'who_introduced', 'bulk_deliveries')
    list_filter = ('date_arrival_point', 'cubage_deliveries', 'arrival_point',
                   'count_deliveries', 'truck_number', 'time_input_date',
                   'who_introduced', 'bulk_deliveries')


@admin.register(Wood)
class LogAdmin(admin.ModelAdmin):
    list_display = ('name_wood', 'size_wood', 'cubage',
                    'count', 'length', 'delivery_number',
                    'nature_size')
    list_filter = ('name_wood', 'size_wood', 'cubage',
                   'count', 'length', 'delivery_number',
                   'nature_size')


@admin.register(TypeOfWood)
class TypeOfLogsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('name_wood', 'size_wood', 'cubage', 'count', 'length', 'date_realization')
    list_filter = ('name_wood', 'size_wood', 'cubage', 'count', 'length', 'date_realization')


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('name_wood', 'size_wood', 'cubage', 'count', 'length')
    list_filter = ('name_wood', 'size_wood', 'cubage', 'count', 'length')

