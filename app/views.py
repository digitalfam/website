from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from datetime import date



@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        pass

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        try:
            employee = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            employee = None
        parents = Parents.objects.filter(user=user)
        context = {
            'user': user,
            'profile': profile,
            'employee': employee,
            'parents': parents,
        }
        return render(request, 'profile.html', context)

    def post(self, request):
        # Lógica para atualização do perfil pode ser implementada aqui.
        pass
    
@method_decorator(staff_member_required, name='dispatch')
class EmployeeView(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            employees = Employee.objects.filter(user__first_name__icontains=search_query).order_by('user__first_name')
        else:
            employees = Employee.objects.all().order_by('user__first_name')
        return render(request, 'employees.html', {'employees': employees, 'search': search_query})
       
@method_decorator(login_required, name='dispatch')
class CreateEmployeeView(View):
    def get(self, request):
        form = EmployeeCreationForm()
        employees = Employee.objects.all()
        occupations = Occupation.objects.all()
        return render(request, 'createEmployee.html', {'form': form, 'employees': employees, 'occupations': occupations})

    def post(self, request):
        form = EmployeeCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Funcionário criado com sucesso!', extra_tags="redirect")
                return redirect('employee')  # Substitua pelo nome da sua URL de listagem
            except IntegrityError as e:
                messages.error(request, f'Erro ao criar funcionário: {e}')
        else:
            messages.error(request, 'Erro ao criar funcionário. Verifique os dados inseridos.', extra_tags="redirect")
        employees = Employee.objects.all()
        occupations = Occupation.objects.all()
        return render(request, 'createEmployee.html', {'form': form, 'employees': employees, 'occupations': occupations})


    
@method_decorator(staff_member_required, name='dispatch')
class DeleteEmployeeView(View):
    def post(self, request, pk):
        employee = Employee.objects.get(id=pk)
        employee.delete()
        messages.success(request, 'Funcionário deletado com sucesso!', extra_tags="redirect")
        return redirect('employee')

@method_decorator(staff_member_required, name='dispatch')
class UpdateEmployeeView(View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        profile = get_object_or_404(Profile, user=employee.user)
        user_obj = employee.user
        employee_form = EmployeeUpdateForm(instance=employee)
        profile_form = ProfileUpdateForm(instance=profile)
        user_form = UserUpdateForm(instance=user_obj)
        context = {
            'employee': employee,
            'user': user_obj,
            'employee_form': employee_form,
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(request, 'updateEmployee.html', context)

    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        profile = get_object_or_404(Profile, user=employee.user)
        user_obj = employee.user
        employee_form = EmployeeUpdateForm(request.POST, request.FILES, instance=employee)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=user_obj)
        if employee_form.is_valid() and profile_form.is_valid() and user_form.is_valid():
            employee_form.save()
            profile_form.save()
            user_form.save()
            messages.success(request, "Funcionário atualizado com sucesso!", extra_tags="redirect")
            return redirect('employee')
        context = {
            'employee': employee,
            'user': user_obj,
            'employee_form': employee_form,
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(request, 'employee.html', context)

@method_decorator(staff_member_required, name='dispatch')
class EmployeeDetailView(View):
    def get(self, request, id):
        employee = Employee.objects.get(id=id)
        documents = DocumentEmployee.objects.filter(employee=employee)
        profile = Profile.objects.get(user=employee.user)
        return render(request, 'detailEmployee.html', {'employee': employee, 'documents': documents, 'profile': profile})

@method_decorator(staff_member_required, name='dispatch')
class CreateEmployeeDocumentView(View):
    def get(self, request, employee_pk):
        employee = get_object_or_404(Employee, pk=employee_pk)
        # Preenche o campo 'employee' e pode ocultá-lo no template, se desejado.
        form = DocumentEmployeeForm(initial={'employee': employee.pk})
        return render(request, 'createEmployeeDocument.html', {
            'employee': employee,
            'form': form,
        })

    def post(self, request, employee_pk):
        employee = get_object_or_404(Employee, pk=employee_pk)
        form = DocumentEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.employee = employee
            document.save()
            # Redirecione para uma página desejada, p. ex. detalhes do funcionário.
            return redirect('employee_detail', id=employee.pk)
        return render(request, 'createEmployeeDocument.html', {
            'employee': employee,
            'form': form,
        })
        

    
@method_decorator(login_required, name='dispatch')
class StudentView(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            students = Students.objects.filter(name__icontains=search_query).order_by('name')
        else:
            students = Students.objects.all().order_by('name')
        classes = Class.objects.all()
        student_classes = {student.pk: student.classes.all() for student in students}
        return render(request, 'students.html', {
            'students': students,
            'classes': classes,
            'student_classes': student_classes,
            'search': search_query,
        })
        
@method_decorator(staff_member_required, name='dispatch')     
class CreateStudentView(View):
    def get(self, request):
        student_form = StudentForm()
        return render(request, 'createStudent.html', {
            'student_form': student_form,
        })

    def post(self, request):
        student_form = StudentForm(request.POST, request.FILES)
        if student_form.is_valid():
            student_form.save()
            messages.success(request, 'Aluno criado com sucesso!', extra_tags="redirect")
            return redirect('student')  # Redirecione para a lista de alunos após o cadastro
        messages.error(request, 'Erro ao criar aluno. Verifique os dados inseridos.', extra_tags="redirect")
        print(student_form.errors)
        return render(request, 'createStudent.html', {
            'student_form': student_form,
        })

@method_decorator(staff_member_required, name='dispatch')
class CreateStudentDocumentView(View):
    def get(self, request, student_pk):
        student = get_object_or_404(Students, pk=student_pk)
        form = DocumentStudentForm(initial={'student': student.pk})
        return render(request, 'createStudentDocument.html', {
            'student': student,
            'form': form,
        })

    def post(self, request, student_pk):
        student = get_object_or_404(Students, pk=student_pk)
        form = DocumentStudentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.student = student
            document.save()
            return redirect('student')
        return render(request, 'createStudentDocument.html', {
            'student': student,
            'form': form,
        })
        
@method_decorator(login_required, name='dispatch')
class StudentDetailView(View):
    def get(self, request, id):
        student = Students.objects.get(id=id)
        documents = DocumentStudent.objects.filter(student=student)
        return render(request, 'detailStudent.html', {'student': student, 'documents': documents})
    
@method_decorator(staff_member_required, name='dispatch')
class DeleteStudentView(View):
    def post(self, request, pk):
        student = Students.objects.get(id=pk)
        student.delete()
        messages.success(request, 'Aluno deletado com sucesso!', extra_tags="redirect")
        return redirect('student')
    
@method_decorator(staff_member_required, name='dispatch')
class UpdateStudentView(View):
    def get(self, request, pk):
        student = get_object_or_404(Students, pk=pk)
        form = StudentUpdateForm(instance=student)
        return render(request, 'updateStudent.html', {'student_form': form, 'student': student})

    def post(self, request, pk):
        student = get_object_or_404(Students, pk=pk)
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Aluno atualizado com sucesso!", extra_tags="redirect")
            return redirect('student')  # Redirecione para a lista de alunos ou detalhe do aluno
        messages.error(request, "Erro ao atualizar aluno. Verifique os dados informados.", extra_tags="redirect")
        return render(request, 'updateStudent.html', {'student_form': form, 'student': student})
    
@method_decorator(staff_member_required, name='dispatch')
class ClassView(View):
    def get(self, request):
        classes = Class.objects.all
        return render(request, 'class.html', {'classes': classes})

@method_decorator(staff_member_required, name='dispatch')
class CreateClassView(View):
    def get(self, request):
        form = ClassForm()
        students = Students.objects.all()
        return render(request, 'createClass.html', {'form': form, 'students': students})

    def post(self, request):
        form = ClassForm(request.POST, request.FILES)  # Certifique-se de passar request.FILES aqui
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma criada com sucesso!', extra_tags="redirect")
            return redirect('class')  # Redirecione para a lista de turmas ou outra página desejada
        messages.error(request, 'Erro ao criar turma. Verifique os dados inseridos.', extra_tags="redirect")
        students = Students.objects.all()
        return render(request, 'createClass.html', {'form': form, 'students': students})

@method_decorator(staff_member_required, name='dispatch')
class DeleteClassView(View):
    def get(self, request, pk):
        return self.post(request, pk)

    def post(self, request, pk):
        class_obj = Class.objects.get(id=pk)
        class_obj.delete()
        messages.success(request, 'Turma deletada com sucesso!', extra_tags="redirect")
        return redirect('class')
    

class HistoryAttendanceView(View):
    def get(self, request, turma_id):
        turma = get_object_or_404(Class, pk=turma_id)
        attendances = AttendanceStudents.objects.filter(turma=turma).order_by('date')
        attendance_by_date = {}
        for attendance in attendances:
            if attendance.date not in attendance_by_date:
                attendance_by_date[attendance.date] = []
            attendance_by_date[attendance.date].append(attendance)
        return render(request, 'attendance_history.html', {'turma': turma, 'attendance_by_date': attendance_by_date})
    
class TakeAttendanceView(View):
    def get(self, request, turma_id):
        turma = get_object_or_404(Class, pk=turma_id)
        today = timezone.now().date()
        if AttendanceStudents.objects.filter(turma=turma, date=today).exists():
            messages.error(request, "A frequência para hoje já foi registrada.", extra_tags="redirect")
        attendances = AttendanceStudents.objects.filter(turma=turma, date=today)
        attendance_dict = {record.student.pk: record for record in attendances}
        return render(request, 'attendance.html', {'turma': turma, 'students': turma.students.all(), 'attendance': attendance_dict})

    def post(self, request, turma_id):
        turma = get_object_or_404(Class, pk=turma_id)
        today = timezone.now().date()
        if AttendanceStudents.objects.filter(turma=turma, date=today).exists():
            messages.error(request, "A frequência para hoje já foi registrada.", extra_tags="redirect")
            return redirect('history_attendance', turma_id=turma_id)
        present_ids = request.POST.getlist('present')
        for student in turma.students.all():
            AttendanceStudents.objects.update_or_create(
                turma=turma,
                student=student,
                date=today,
                defaults={'present': str(student.pk) in present_ids}
            )
        messages.success(request, "Frequência registrada com sucesso!", extra_tags="redirect")
        return redirect('history_attendance', turma_id=turma_id)