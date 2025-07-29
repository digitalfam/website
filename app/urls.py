from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create_employee/', CreateEmployeeView.as_view(), name='create_employee'),
    path('employees/', EmployeeView.as_view(), name='employees'),
    path('delete_employee/<int:employee_pk>/', DeleteEmployeeView.as_view(), name='delete_employee'),
    path('update_employee/<int:employee_pk>/', UpdateEmployeeView.as_view(), name='update_employee'),
    path('detail_employee/<int:employee_pk>/', EmployeeDetailView.as_view(), name='detail_employee'),
    path('create_employee_document/<int:employee_pk>/', CreateEmployeeDocumentView.as_view(), name='create_employee_document'),
    path('students/', StudentView.as_view(), name='students'),
    path('create_student/', CreateStudentView.as_view(), name='create_student'),
    path('create_student_document/<int:student_pk>/', CreateStudentDocumentView.as_view(), name='create_student_document'),
    path('detail_student/<int:student_pk>/', StudentDetailView.as_view(), name='detail_student'),
    path('delete_student/<int:student_pk>/', DeleteStudentView.as_view(), name='delete_student'),
    path('update_student/<int:student_pk>/', UpdateStudentView.as_view(), name='update_student'),
    path('class/', ClassView.as_view(), name='class'),
    path('create_class/', CreateClassView.as_view(), name='create_class'),
    path('delete_class/<int:class_pk>/', DeleteClassView.as_view(), name='delete_class'),
    path('history_attendance/', HistoryAttendanceView.as_view(), name='history_attendance'),
    path('take_attendance/', TakeAttendanceView.as_view(), name='take_attendance'),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        html_email_template_name='password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
