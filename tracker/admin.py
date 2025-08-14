from django.contrib import admin
from .models import Project, Laborer, DailyProgress, Expense


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_date', 'end_date', 'total_labor_cost', 'total_expenses')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'location')


@admin.register(Laborer)
class LaborerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'daily_rate', 'assigned_project')
    list_filter = ('role', 'assigned_project')
    search_fields = ('name',)


@admin.register(DailyProgress)
class DailyProgressAdmin(admin.ModelAdmin):
    list_display = ('project', 'date', 'summary')
    list_filter = ('date', 'project')
    search_fields = ('summary',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('project', 'category', 'amount', 'date')
    list_filter = ('category', 'date', 'project')
    search_fields = ('notes',)