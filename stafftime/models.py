# coding=utf-8

from django.db import models
from datetime import datetime, timedelta

DEFAULT_DEP_ID = 1
DEFAULT_EMP_ID = 1


class Department(models.Model):
    name = models.CharField('Отделение', max_length=300)

    def __str__(self):
        return self.name.encode('utf-8')


class Employee(models.Model):
    first_name = models.CharField('Имя', max_length=250)
    second_name = models.CharField("Фамилия", max_length=250)
    hire_date = models.DateField("Дата наема (ГГ-ММ-ДД)", default=datetime.now)
    department = models.ForeignKey(Department, default=DEFAULT_DEP_ID)

    def __str__(self):
        return self.first_name.encode('utf-8') + " " + self.second_name.encode('utf-8')


class Timeline(models.Model):
    department = models.ForeignKey(Department, default=DEFAULT_DEP_ID)
    turn = models.CharField("Вид смены", max_length=128)
    start_time = models.TimeField('Время начала')
    end_time = models.TimeField("Время завершения")


class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(Employee, default=DEFAULT_EMP_ID)
    arriving_time = models.TimeField('Время прихода', editable=True)
    leaving_time = models.TimeField("Время ухода", editable=True)
    current_day = models.DateField("День (ГГ-ММ-ДД)", default=datetime.now)


class DateSearch(models.Model):
    date_search = models.DateTimeField('Найти по дате:')