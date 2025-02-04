from django.contrib import admin
from .models import Occupation, DocumentEmployee, DocumentStudent, DocumentParent, Employee, Profile, Students, Class, AttendanceStudents, Parents, AuditLog

@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name']

# Inlines para documentos
class DocumentEmployeeInline(admin.TabularInline):
    model = DocumentEmployee
    extra = 1
    readonly_fields = ('uploaded_at',)
    show_change_link = True

class DocumentStudentInline(admin.TabularInline):
    model = DocumentStudent
    extra = 1
    readonly_fields = ('uploaded_at',)
    show_change_link = True

class DocumentParentInline(admin.TabularInline):
    model = DocumentParent
    extra = 1
    readonly_fields = ('uploaded_at',)
    show_change_link = True

# Inline para Employee no UserAdmin (Opcional)
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Funcionário'
    fk_name = 'user'



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'cpf', 'phone', 'city', 'created_at', 'has_employee')
    search_fields = ('user__username', 'cpf', 'phone')
    list_filter = ('role', 'city', 'created_at')
    ordering = ['user__username']
    # Se deseja editar Employee diretamente no ProfileAdmin, adicione como inline
    # inlines = [EmployeeInline]

    def has_employee(self, obj):
        return hasattr(obj, 'employee')
    has_employee.boolean = True
    has_employee.short_description = 'Tem Funcionário?'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'occupation', 'salary', 'admission', 'resignation')
    search_fields = ('user__username', 'occupation__name')
    list_filter = ('occupation', 'admission', 'resignation')
    ordering = ['user__username']
    inlines = [DocumentEmployeeInline]

@admin.register(DocumentEmployee)
class DocumentEmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'uploaded_at')
    search_fields = ('employee__user__username', 'title')
    list_filter = ('uploaded_at',)
    ordering = ['-uploaded_at']

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('enrollment_number','name', 'last_name', 'birth_date', 'city', 'emergency_phone','observations', 'created_at')
    search_fields = ('name', 'last_name', 'city')
    list_filter = ('city', 'created_at')
    ordering = ['name', 'last_name']
    inlines = [DocumentStudentInline]

@admin.register(DocumentStudent)
class DocumentStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'uploaded_at')
    search_fields = ('student__name', 'student__last_name', 'title')
    list_filter = ('uploaded_at',)
    ordering = ['-uploaded_at']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'shift','image', 'created_at')
    search_fields = ('name', 'teacher__username')
    list_filter = ('shift', 'created_at')
    ordering = ['name']

@admin.register(AttendanceStudents)
class AttendanceStudentsAdmin(admin.ModelAdmin):
    list_display = ('turma', 'student', 'date', 'present', 'created_at')
    search_fields = ('turma__name', 'student__name', 'student__last_name')
    list_filter = ('turma', 'present', 'date')
    ordering = ['-date']
    date_hierarchy = 'date'
    actions = ['mark_as_present', 'mark_as_absent']

    def mark_as_present(self, request, queryset):
        queryset.update(present=True)
    mark_as_present.short_description = "Marcar selecionados como Presentes"

    def mark_as_absent(self, request, queryset):
        queryset.update(present=False)
    mark_as_absent.short_description = "Marcar selecionados como Ausentes"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        turma_id = request.GET.get('turma__id__exact')
        if turma_id:
            extra_context['title'] = f'Attendance for Turma {turma_id}'
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        turma_id = request.GET.get('turma__id__exact')
        if turma_id:
            qs = qs.filter(turma_id=turma_id)
        return qs

@admin.register(Parents)
class ParentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_sons', 'created_at')
    search_fields = ('user__username', 'sons__name', 'sons__last_name')
    list_filter = ('created_at',)
    ordering = ['user__username']
    inlines = [DocumentParentInline]

    def get_sons(self, obj):
        return ", ".join([f"{son.name} {son.last_name}" for son in obj.son.all()])
    get_sons.short_description = 'Filhos'

@admin.register(DocumentParent)
class DocumentParentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'title', 'uploaded_at')
    search_fields = ('parent__user__username', 'title')
    list_filter = ('uploaded_at',)
    ordering = ['-uploaded_at']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'model_name', 'object_id', 'action', 'timestamp')
    search_fields = ('user__username', 'model_name', 'action')
    list_filter = ('model_name', 'action', 'timestamp')
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'

