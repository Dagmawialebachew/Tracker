from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from .models import Project, Laborer, DailyProgress, Expense


class DashboardView(TemplateView):
    template_name = 'tracker/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.all()
        
        context.update({
            'projects': projects[:5],  # Show recent 5 projects
            'total_projects': projects.count(),
            'active_projects': projects.filter(end_date__gte='2024-01-01').count(),
            'total_laborers': Laborer.objects.count(),
            'recent_progress': DailyProgress.objects.all()[:5],
            'recent_expenses': Expense.objects.all()[:5],
        })
        return context


# Project Views
class ProjectListView(ListView):
    model = Project
    template_name = 'tracker/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'tracker/project_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context.update({
            'laborers': project.laborer_set.all(),
            'progress_entries': project.dailyprogress_set.all()[:5],
            'expenses': project.expense_set.all()[:5],
        })
        return context


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'tracker/project_form.html'
    fields = ['name', 'location', 'start_date', 'end_date']
    success_url = reverse_lazy('project_list')


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'tracker/project_form.html'
    fields = ['name', 'location', 'start_date', 'end_date']
    success_url = reverse_lazy('project_list')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'tracker/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')


class ProjectReportView(DetailView):
    model = Project
    template_name = 'tracker/project_report.html'
    
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
class LaborerListView(ListView):
    model = Laborer
    template_name = 'tracker/laborer_list.html'
    context_object_name = 'laborers'
    paginate_by = 10


class LaborerDetailView(DetailView):
    model = Laborer
    template_name = 'tracker/laborer_detail.html'


class LaborerCreateView(CreateView):
    model = Laborer
    template_name = 'tracker/laborer_form.html'
    fields = ['name', 'role', 'daily_rate', 'assigned_project']
    success_url = reverse_lazy('laborer_list')


class LaborerUpdateView(UpdateView):
    model = Laborer
    template_name = 'tracker/laborer_form.html'
    fields = ['name', 'role', 'daily_rate', 'assigned_project']
    success_url = reverse_lazy('laborer_list')


class LaborerDeleteView(DeleteView):
    model = Laborer
    template_name = 'tracker/laborer_confirm_delete.html'
    success_url = reverse_lazy('laborer_list')


# Progress Views
class ProgressListView(ListView):
    model = DailyProgress
    template_name = 'tracker/progress_list.html'
    context_object_name = 'progress_entries'
    paginate_by = 10


class ProgressDetailView(DetailView):
    model = DailyProgress
    template_name = 'tracker/progress_detail.html'


class ProgressCreateView(CreateView):
    model = DailyProgress
    template_name = 'tracker/progress_form.html'
    fields = ['date', 'project', 'summary', 'optional_photo']
    success_url = reverse_lazy('progress_list')


class ProgressUpdateView(UpdateView):
    model = DailyProgress
    template_name = 'tracker/progress_form.html'
    fields = ['date', 'project', 'summary', 'optional_photo']
    success_url = reverse_lazy('progress_list')


class ProgressDeleteView(DeleteView):
    model = DailyProgress
    template_name = 'tracker/progress_confirm_delete.html'
    success_url = reverse_lazy('progress_list')


# Expense Views
class ExpenseListView(ListView):
    model = Expense
    template_name = 'tracker/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10


class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'tracker/expense_detail.html'


class ExpenseCreateView(CreateView):
    model = Expense
    template_name = 'tracker/expense_form.html'
    fields = ['date', 'project', 'category', 'amount', 'notes']
    success_url = reverse_lazy('expense_list')


class ExpenseUpdateView(UpdateView):
    model = Expense
    template_name = 'tracker/expense_form.html'
    fields = ['date', 'project', 'category', 'amount', 'notes']
    success_url = reverse_lazy('expense_list')


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = 'tracker/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')