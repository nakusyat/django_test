from django.conf.urls import patterns, url
from .views import IndexView, EditDepartmentView, EditEmployeeView, DeleteEmployeeView, DeleteDepartmentView, \
    AddTimelineView, TimelineView, EditTimelineView, DeleteTimelineView, AddEmployeeAttendanceView, \
    EmployeeAttendanceView, EditEmployeeAttendanceView, DeleteEmployeeAttendanceView, EmployeeAttendanceSearchView, \
    EmployeeAttendanceReportView
from .views import EmployeeView
from .views import DepartmentView
from .views import AddEmployeeView
from .views import AddDepartmentView


urlpatterns = patterns('',
    url(r'^employee/add', AddEmployeeView.as_view(), name='create_employee'),
    url(r'^employee/search', EmployeeView.as_view(), name='search_employee'),
    url(r'^employee/(?P<emp_id>.*)/edit$', EditEmployeeView.as_view(), name='edit_employee'),
    url(r'^employee/(?P<emp_id>.*)/delete', DeleteEmployeeView.as_view(), name='delete_employee'),
    url(r'^employee/(?P<emp_type>.*)/all', EmployeeView.as_view(), name='emp'),
    url(r'^department/add', AddDepartmentView.as_view(), name='create_department'),
    url(r'^department/(?P<dep_id>.*)/edit$', EditDepartmentView.as_view(), name='edit_department'),
    url(r'^department/(?P<dep_id>.*)/delete$', DeleteDepartmentView.as_view(), name='delete_department'),
    url(r'^department/', DepartmentView.as_view(), name='dep'),
    url(r'^timeline/add', AddTimelineView.as_view(), name='create_timeline'),
    url(r'^timeline/(?P<timeline_id>.*)/edit$', EditTimelineView.as_view(), name='edit_timeline'),
    url(r'^timeline/(?P<timeline_id>.*)/delete$', DeleteTimelineView.as_view(), name='delete_timeline'),
    url(r'^timeline/(?P<timeline_type>.*)/all', TimelineView.as_view(), name='timeline'),
    url(r'^empatt/add', AddEmployeeAttendanceView.as_view(), name='create_empatt'),
    url(r'^empatt/search', EmployeeAttendanceSearchView.as_view(), name='search_by_filter'),
    url(r'^empatt/(?P<empatt_id>.*)/edit$', EditEmployeeAttendanceView.as_view(), name='edit_empatt'),
    url(r'^empatt/(?P<empatt_id>.*)/delete$', DeleteEmployeeAttendanceView.as_view(), name='delete_empatt'),
    url(r'^empatt/(?P<empatt_type>.*)/all', EmployeeAttendanceView.as_view(), name='empatt'),
    url(r'^report', EmployeeAttendanceReportView.as_view(), name='report'),
    url(r'^$', EmployeeView.as_view(), name='home'),
)

