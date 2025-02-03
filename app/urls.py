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
    path('delete_employee/<int:pk>/', DeleteEmployeeView.as_view(), name='delete_employee'),
    path('update_employee/<int:pk>/', UpdateEmployeeView.as_view(), name='update_employee'),
    path('employee_detail/<int:id>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employee/<int:employee_pk>/document/create/', CreateEmployeeDocumentView.as_view(), name='create_employee_document'),
    path('employee/', EmployeeView.as_view(), name='employee'),
    path('student/', StudentView.as_view(), name='student'),
    path('create_student/', CreateStudentView.as_view(), name='create_student'),
    path('create_student_document/<int:student_pk>/', CreateStudentDocumentView.as_view(), name='create_student_document'),
    path('student_detail/<int:id>/', StudentDetailView.as_view(), name='student_detail'),
    path('delete_student/<int:pk>/', DeleteStudentView.as_view(), name='delete_student'),
    path('update_student/<int:pk>/', UpdateStudentView.as_view(), name='update_student'),
    path('class/', ClassView.as_view(), name='class'),
    path('create_class/', CreateClassView.as_view(), name='create_class'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        html_email_template_name='password_reset_email.html',
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
