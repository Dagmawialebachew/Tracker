from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Laborer, Attendance
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import Project, Laborer, DailyProgress, Expense, Attendance
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker/dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to access the dashboard.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.filter(user=self.request.user)
        
        context.update({
            'projects': projects[:5],  # Show recent 5 projects
            'total_projects': projects.count(),
            'active_projects': projects.filter(end_date__gte='2024-01-01').count(),
            'total_laborers': Laborer.objects.filter(assigned_project__user=self.request.user).count(),
            'recent_progress': DailyProgress.objects.filter(project__user=self.request.user)[:5],
            'recent_expenses': Expense.objects.filter(project__user=self.request.user)[:5],
        })
        return context

# Project Views
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tracker/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view your projects.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter projects by logged-in user
        return Project.objects.filter(user=self.request.user)

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'tracker/project_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view project details.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context.update({
            'laborers': project.laborer_set.all(),
            'progress_entries': project.dailyprogress_set.all()[:5],
            'expenses': project.expense_set.all()[:5],
        })
        return context

    def test_func(self):
        # Only allow the owner to access
        project = self.get_object()
        return project.user == self.request.user

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'tracker/project_form.html'
    fields = ['name', 'location', 'start_date', 'end_date']
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to create a project.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user  # assign the logged-in user
        return super().form_valid(form)



class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'tracker/project_form.html'
    fields = ['name', 'location', 'start_date', 'end_date']
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to update a project.")
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        project = self.get_object()
        return project.user == self.request.user



class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'tracker/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to delete a project.")
        return super().dispatch(request, *args, **kwargs)


class ProjectReportView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'tracker/project_report.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view project reports.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Calculate expenses by category
        expenses_by_category = project.expense_set.values('category').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        context.update({
            'expenses_by_category': expenses_by_category,
            'material_cost': project.expense_set.filter(
                category='materials'
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
        })
        return context


# Laborer Views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class LaborerListView(LoginRequiredMixin, ListView):
    model = Laborer
    template_name = 'tracker/laborer_list.html'
    context_object_name = 'laborers'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view laborers.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Only laborers assigned to projects owned by the logged-in user
        return Laborer.objects.filter(assigned_project__user=self.request.user)



class LaborerDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Laborer
    template_name = 'tracker/laborer_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view laborer details.")
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        laborer = self.get_object()
        return laborer.assigned_project.user == self.request.user



class LaborerCreateView(LoginRequiredMixin, CreateView):
    model = Laborer
    template_name = 'tracker/laborer_form.html'
    fields = ['name', 'role', 'daily_rate', 'assigned_project']
    success_url = reverse_lazy('laborer_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to add a laborer.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Only allow selection of projects owned by the user
        form.fields['assigned_project'].queryset = Project.objects.filter(user=self.request.user)
        return form



class LaborerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Laborer
    template_name = 'tracker/laborer_form.html'
    fields = ['name', 'role', 'daily_rate', 'assigned_project']
    success_url = reverse_lazy('laborer_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to update a laborer.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['assigned_project'].queryset = Project.objects.filter(user=self.request.user)
        return form

    def test_func(self):
        laborer = self.get_object()
        return laborer.assigned_project.user == self.request.user



class LaborerDeleteView(LoginRequiredMixin, DeleteView):
    model = Laborer
    template_name = 'tracker/laborer_confirm_delete.html'
    success_url = reverse_lazy('laborer_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to delete a laborer.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Only allow deletion of laborers assigned to projects owned by the user
        return Laborer.objects.filter(assigned_project__user=self.request.user)


# Progress Views
class ProgressListView(LoginRequiredMixin,ListView):
    model = DailyProgress
    template_name = 'tracker/progress_list.html'
    context_object_name = 'progress_entries'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view progress entries.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter progress entries by projects owned by the logged-in user
        return DailyProgress.objects.filter(project__user=self.request.user)


class ProgressDetailView(LoginRequiredMixin, DetailView):
    model = DailyProgress
    template_name = 'tracker/progress_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view progress details.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        progress_entry = self.get_object()
        context.update({
            'project': progress_entry.project,
        })
        return context


class ProgressCreateView(LoginRequiredMixin, CreateView):
    model = DailyProgress
    template_name = 'tracker/progress_form.html'
    fields = ['date', 'project', 'summary', 'optional_photo']
    success_url = reverse_lazy('progress_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to add progress.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Only allow selection of projects owned by the user
        form.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        return form


class ProgressUpdateView(LoginRequiredMixin, UpdateView):
    model = DailyProgress
    template_name = 'tracker/progress_form.html'
    fields = ['date', 'project', 'summary', 'optional_photo']
    success_url = reverse_lazy('progress_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to update progress.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        return form

class ProgressDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyProgress
    template_name = 'tracker/progress_confirm_delete.html'
    success_url = reverse_lazy('progress_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to delete progress.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Only allow deletion of progress entries for projects owned by the user
        return DailyProgress.objects.filter(project__user=self.request.user)


# Expense Views
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'tracker/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view expenses.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter expenses by projects owned by the logged-in user
        return Expense.objects.filter(project__user=self.request.user)


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'tracker/expense_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view expense details.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense = self.get_object()
        context.update({
            'project': expense.project,
        })
        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'tracker/expense_form.html'
    fields = ['date', 'project', 'category', 'amount', 'notes']
    success_url = reverse_lazy('expense_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to add an expense.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Only allow selection of projects owned by the user
        form.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        return form


class ExpenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Expense
    template_name = 'tracker/expense_form.html'
    fields = ['date', 'project', 'category', 'amount', 'notes']
    success_url = reverse_lazy('expense_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to update an expense.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        return form

    def test_func(self):
        expense = self.get_object()
        return expense.project.user == self.request.user


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'tracker/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to delete an expense.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Only allow deletion of expenses for projects owned by the user
        return Expense.objects.filter(project__user=self.request.user)
    
    
#Handling the Attendance

class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'tracker/attendance_list.html'
    context_object_name = 'attendances'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to view attendance records.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter attendance records by projects owned by the logged-in user
        return Attendance.objects.filter(laborer__assigned_project__user=self.request.user)

class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    template_name = 'tracker/attendance_form.html'
    fields = ['laborer', 'date', 'project']
    success_url = reverse_lazy('attendance_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must log in to add attendance records.")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Only allow selection of laborers assigned to projects owned by the user
        form.fields['laborer'].queryset = Laborer.objects.filter(assigned_project__user=self.request.user)
        form.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        return form
    
    
class LaborerAttendanceView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'tracker/laborer_attendance.html'
    context_object_name = 'attendances'

    def get_queryset(self):
        # Get the laborer ID from the URL
        laborer_id = self.kwargs['pk']
        return Attendance.objects.filter(laborer__id=laborer_id).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        laborer_id = self.kwargs['pk']
        context['laborer'] = Laborer.objects.get(id=laborer_id)
        return context
    
    
    
class LaborerCheckInView(LoginRequiredMixin, View):
    def get(self, request, pk):
        laborer = get_object_or_404(Laborer, pk=pk)
        today = timezone.localdate()
        attendance, created = Attendance.objects.get_or_create(
            laborer=laborer,
            project=laborer.assigned_project,
            date=today,
            defaults={'status': 'Absent'}
        )
        attendance.status = 'Present'
        attendance.save()
        messages.success(request, f"{laborer.name} checked in successfully for today!")
        return redirect('laborer_attendance', pk=laborer.pk)