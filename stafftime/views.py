# coding=utf-8
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Employee, Timeline, EmployeeAttendance
from .models import Department
from .forms import EmployeeForm, TimelineForm, SearchForm, EmployeeAttendanceForm, DateSearchForm, \
    AttendanceReportSearchForm
from .forms import DepartmentForm


class DepartmentView(View):

    template_dir = "stafftime/department/index.html"

    def dispatch(self, request, *args, **kwargs):

        departments = Department.objects.all().order_by('name')
        paginator = Paginator(departments, 2)
        page = request.GET.get('page')
        try:
            departments = paginator.page(page)
        except PageNotAnInteger:
            departments = paginator.page(1)
        except EmptyPage:
            departments = paginator.page(paginator.num_pages)

        return render(request, self.template_dir, {
                'departments': departments
            })


class AddDepartmentView(View):
    template_dir = "stafftime/department/create.html"

    def dispatch(self, request, *args, **kwargs):
        department_form = DepartmentForm()
        if request.method == "POST":
            department_form = DepartmentForm(request.POST)
            if department_form.is_valid():
                if department_form.save():
                    messages.success(request, "Успешно добавлено новое отделение")
        return render(request, self.template_dir,
        {
            'form': department_form,
        })


class EditDepartmentView(View):
    template_dir = "stafftime/department/edit.html"

    def dispatch(self, request, *args, **kwargs):
        department = Department.objects.get(pk=kwargs['dep_id'])
        department_form = DepartmentForm(instance=department)
        if request.method == "POST":
            department_form = DepartmentForm(request.POST, instance=department)
            if department_form.is_valid():
                if department_form.save():
                    messages.success(request, "Отделение успешно изменено")

        return render(request, self.template_dir,
        {
            'form': department_form,
            'dep_id':department.id
        })


class DeleteDepartmentView(View):

    def dispatch(self, request, *args, **kwargs):
        if kwargs['dep_id']:
            Department.objects.filter(id=kwargs['dep_id']).delete()

        return redirect(reverse('timeline:dep'))


class EmployeeView(View):
    template_dir = "stafftime/employee/index.html"

    def dispatch(self, request, *args, **kwargs):

        if 'emp_type' in kwargs:
            type = str(kwargs['emp_type'])
        else:
            type = 'first_name'

        employees = Employee.objects.all().order_by(type)
        search_form = SearchForm()

        if request.method == "POST":
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                departments = Department.objects.filter(name__contains=search_form.cleaned_data['criteria_value'])
                employees = Employee.objects.filter(Q(first_name__contains=search_form.cleaned_data['criteria_value']) | Q(department=departments))

        return render(request, self.template_dir,
            {
                'employees': employees,
                'form': search_form
            })


class AddEmployeeView(View):
    template_dir = "stafftime/employee/create.html"

    def dispatch(self, request, *args, **kwargs):
        employee_form = EmployeeForm()
        if request.method == "POST":
            employee_form = EmployeeForm(request.POST)
            if employee_form.is_valid():
                if employee_form.save():
                    messages.success(request, "Успешно добавлен новый сотрудник")

        return render(request, self.template_dir,
        {
            'form': employee_form
        })


class EditEmployeeView(View):
    template_dir = "stafftime/employee/edit.html"

    def dispatch(self, request, *args, **kwargs):
        employee = Employee.objects.get(pk=kwargs['emp_id'])
        employee_form = EmployeeForm(instance=employee)

        if request.method == "POST":
            employee_form = EmployeeForm(request.POST, instance=employee)
            if employee_form.is_valid():
                if employee_form.save():
                    messages.success(request, "Успешно изменен сотрудник")

        return render(request, self.template_dir,
        {
            'emp_id': employee.id,
            'form': employee_form
        })


class DeleteEmployeeView(View):

    def dispatch(self, request, *args, **kwargs):
        if 'emp_id' in kwargs:
            Employee.objects.filter(id=kwargs['emp_id']).delete()

        return redirect(reverse('timeline:emp', kwargs={'emp_type':'first_name'}))


class AddTimelineView(View):
    template_dir = "stafftime/timeline/create.html"

    def dispatch(self, request, *args, **kwargs):
        timeline_form = TimelineForm()
        if request.method == "POST":
            timeline_form = TimelineForm(request.POST)
            if timeline_form.is_valid():
                if timeline_form.save():
                    messages.success(request, "Успешно добавлено новое расписание")

        return render(request, self.template_dir,
        {
            'form': timeline_form
        })


class TimelineView(View):
    template_dir = "stafftime/timeline/index.html"

    def dispatch(self, request, *args, **kwargs):

        if kwargs['timeline_type']:
            type = str(kwargs['timeline_type'])
        else:
            type = 'department'

        timelines = Timeline.objects.all().order_by(type)

        return render(request, self.template_dir,
            {
                'timelines': timelines
            })


class EditTimelineView(View):
    template_dir = "stafftime/timeline/edit.html"

    def dispatch(self, request, *args, **kwargs):
        timeline = Timeline.objects.get(pk=kwargs['timeline_id'])
        timeline_form = TimelineForm(instance=timeline)

        if request.method == "POST":
            timeline_form = TimelineForm(request.POST, instance=timeline)
            if timeline_form.is_valid():
                if timeline_form.save():
                    messages.success(request, "Успешно изменено расписание")

        return render(request, self.template_dir,
        {
            'timeline_id': timeline.id,
            'form': timeline_form
        })


class DeleteTimelineView(View):

    def dispatch(self, request, *args, **kwargs):
        if kwargs['timeline_id']:
            Timeline.objects.filter(id=kwargs['timeline_id']).delete()

        return redirect(reverse('timeline:timeline', kwargs={'timeline_type':'department'}))


class AddEmployeeAttendanceView(View):
    template_dir = "stafftime/empatt/create.html"

    def dispatch(self, request, *args, **kwargs):
        empatt_form = EmployeeAttendanceForm()
        if request.method == "POST":
            empatt_form = EmployeeAttendanceForm(request.POST)
            if empatt_form.is_valid():
                if empatt_form.save():
                    messages.success(request, "Успешно добавлено новое расписание")

        return render(request, self.template_dir,
        {
            'form': empatt_form
        })


class EmployeeAttendanceSearchView(View):
    template_dir = "stafftime/filter/absense.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            date_form = DateSearchForm(request.POST)
            if date_form.is_valid():
                if 'department' in request.POST:
                    date_search = date_form.cleaned_data['date_search']
                    department_id = request.POST['department']

                    response_data = {}
                    response_data['form'] = date_form
                    response_data['criteria_type'] = date_form.cleaned_data['attendance_type']
                    response_data['criteria_type_date'] =  date_search

                    if date_form.cleaned_data['attendance_type'] == 'late':
                        response_data['late_employee'] = EmployeeAttendance.objects.filter(employee__department__timeline__start_time__isnull=False, employee__department__exact=department_id, current_day__exact=str(date_search)).extra(where=['"stafftime_employeeattendance"."arriving_time" > "stafftime_timeline"."start_time"'])
                    elif date_form.cleaned_data['attendance_type'] == 'absense':
                        response_data['absent_employee'] = Employee.objects.filter(department__exact=department_id).exclude(id__in=EmployeeAttendance.objects.filter(employee__department__exact=department_id, current_day__exact=str(date_search)).values_list('employee_id', flat=True))

                    return render(request, "stafftime/filter/absense.html",
                    response_data)


class EmployeeAttendanceReportView(View):
    template_dir = "stafftime/filter/report.html"

    def dispatch(self, request, *args, **kwargs):
        response_data = {}
        response_data['late_employees'] = EmployeeAttendance.objects.filter(employee__department__timeline__start_time__isnull=False).extra(where=['"stafftime_employeeattendance"."arriving_time" > "stafftime_timeline"."start_time"'])
        response_data['form'] = AttendanceReportSearchForm
        if request.method == 'POST':
            response_data['form'] = AttendanceReportSearchForm(request.POST)
            if response_data['form'].is_valid():
                date_search = response_data['form'].cleaned_data['report_date_search']
                response_data['month'] = date_search.strftime('%B')
                department_id = request.POST['department']
                response_data['late_employees'] = EmployeeAttendance.objects.filter(employee__department__timeline__start_time__isnull=False, employee__department__exact=department_id, current_day__month=date_search.month).extra(where=['"stafftime_employeeattendance"."arriving_time" > "stafftime_timeline"."start_time"'])

        return render(request, self.template_dir,
              response_data)


class EmployeeAttendanceView(View):
    template_dir = "stafftime/empatt/index.html"

    def dispatch(self, request, *args, **kwargs):

        if 'empatt_type' in kwargs:
            type = str(kwargs['empatt_type'])
        else:
            type = 'employee__first_name'

        empatts = EmployeeAttendance.objects.all().order_by(type)

        paginator = Paginator(empatts, 2)
        page = request.GET.get('page')
        try:
            empatts = paginator.page(page)
        except PageNotAnInteger:
            empatts = paginator.page(1)
        except EmptyPage:
            empatts = paginator.page(paginator.num_pages)

        date_form = DateSearchForm()

        return render(request, self.template_dir,
            {
                'empatts': empatts,
                'form': date_form,
            })


class EditEmployeeAttendanceView(View):
    template_dir = "stafftime/empatt/edit.html"

    def dispatch(self, request, *args, **kwargs):
        empatt = EmployeeAttendance.objects.get(pk=kwargs['empatt_id'])
        empatt_form = EmployeeAttendanceForm(instance=empatt)

        if request.method == "POST":
            empatt_form = EmployeeAttendanceForm(request.POST, instance=empatt)
            if empatt_form.is_valid():
                if empatt_form.save():
                    messages.success(request, "Успешно изменена запись")

        return render(self.template_dir,
        {
            'empatt_id': empatt.id,
            'form': empatt_form
        })


class DeleteEmployeeAttendanceView(View):

    def dispatch(self, request, *args, **kwargs):
        if kwargs['empatt_id']:
            EmployeeAttendance.objects.filter(id=kwargs['empatt_id']).delete()

        return redirect(reverse('timeline:empatt', kwargs={'empatt_type':'employee'}))