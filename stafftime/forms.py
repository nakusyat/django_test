# coding=utf-8
from datetime import date
from django.forms import ModelForm
from django import forms
from django.forms.extras import SelectDateWidget
from .models import Employee, Timeline, EmployeeAttendance, DateSearch
from .models import Department
from datetimewidget.widgets import DateTimeWidget


class DepartmentForm(ModelForm):
    name = forms.CharField(label="Отделение", error_messages={'required': 'Заполните поле'})

    class Meta:
        model = Department
        fields = '__all__'


class DateInput(forms.DateInput):
     input_type = 'date'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'second_name', 'hire_date', 'department']
        widgets = {
            'hire_date': DateInput(attrs={})
        }


class TimelineForm(ModelForm):
    start_time = forms.TimeField(label="Время начала", widget=forms.TimeInput(format='%H:%M'), initial="09:00")
    end_time = forms.TimeField(label="Время завершения", widget=forms.TimeInput(format='%H:%M'), initial="18:00")

    class Meta:
        model = Timeline
        fields = ['department', 'turn', 'start_time', 'end_time']


options = (
    ('name', 'Имя'),
    ('department', 'Отдел')
)

DEFAULT_DEP_ID = 1


class SearchForm(forms.Form):
    criteria_value = forms.CharField(label='Поиск по имени/отделению')


class EmployeeAttendanceForm(ModelForm):
    arriving_time = forms.TimeField(label="Время прихода", widget=forms.TimeInput(format='%H:%M'), initial="09:00")
    leaving_time = forms.TimeField(label="Время ухода", widget=forms.TimeInput(format='%H:%M'), initial="18:00")

    class Meta:
        model = EmployeeAttendance
        fields = '__all__'


departments = Department.objects.all()

criterias = (
    ('late','Опоздавшие'),
    ('absense','Отсутствующие')
)


class DateSearchForm(forms.Form):
    attendance_type = forms.ChoiceField(label='Состояние', widget=forms.Select, choices=criterias)
    department = forms.ModelChoiceField(label='Отделение', queryset=Department.objects.all(), initial=departments)
    date_search = forms.DateField(label='На дату',
    widget=SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),

    ), initial=date.today()
)


class AttendanceReportSearchForm(forms.Form):
    department = forms.ModelChoiceField(label='Отделение', queryset=Department.objects.all(), initial=departments)
    report_date_search = forms.DateField(label='На дату',
    widget=SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
        years=range(2010, 2020)

    ),initial=date.today()
)