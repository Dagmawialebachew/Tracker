from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/<int:pk>/report/', views.ProjectReportView.as_view(), name='project_report'),
    
    # Laborers
    path('laborers/', views.LaborerListView.as_view(), name='laborer_list'),
    path('laborers/<int:pk>/', views.LaborerDetailView.as_view(), name='laborer_detail'),
    path('laborers/create/', views.LaborerCreateView.as_view(), name='laborer_create'),
    path('laborers/<int:pk>/edit/', views.LaborerUpdateView.as_view(), name='laborer_update'),
    path('laborers/<int:pk>/delete/', views.LaborerDeleteView.as_view(), name='laborer_delete'),
    
    # Daily Progress
    path('progress/', views.ProgressListView.as_view(), name='progress_list'),
    path('progress/<int:pk>/', views.ProgressDetailView.as_view(), name='progress_detail'),
    path('progress/create/', views.ProgressCreateView.as_view(), name='progress_create'),
    path('progress/<int:pk>/edit/', views.ProgressUpdateView.as_view(), name='progress_update'),
    path('progress/<int:pk>/delete/', views.ProgressDeleteView.as_view(), name='progress_delete'),
    
    # Expenses
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/create/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
    
    # Attendance
    
   path('laborers/<int:pk>/attendance/', views.LaborerAttendanceView.as_view(), name='laborer_attendance'),
  path('laborers/<int:pk>/checkin/', views.LaborerCheckInView.as_view(), name='laborer_checkin')

]