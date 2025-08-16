from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # temporarily null=True
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

    @property
    def total_labor_cost(self):
        total = Decimal('0.00')
        for laborer in self.laborer_set.all():
            # Count actual attendance days for each laborer on this project
            attendance_days = laborer.attendance_set.filter(project=self).count()
            total += laborer.daily_rate * attendance_days
        return total

    @property
    def total_expenses(self):
        return sum(expense.amount for expense in self.expense_set.all())

    @property
    def progress_count(self):
        return self.dailyprogress_set.count()


class Laborer(models.Model):
    ROLE_CHOICES = [
        ('foreman', 'Foreman'),
        ('electrician', 'Electrician'),
        ('plumber', 'Plumber'),
        ('carpenter', 'Carpenter'),
        ('mason', 'Mason'),
        ('painter', 'Painter'),
        ('general', 'General Labor'),
        ('operator', 'Equipment Operator'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"

    def get_absolute_url(self):
        return reverse('laborer_detail', kwargs={'pk': self.pk})

    @property
    def total_cost(self):
        # Count attendance days for this laborer on their assigned project only
        attendance_days = self.attendance_set.filter(project=self.assigned_project).count()
        return self.daily_rate * attendance_days
    
    @property
    def attendance_days(self):
        return self.attendance_set.filter(project=self.assigned_project).count

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    laborer = models.ForeignKey(Laborer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.laborer.name} - {self.date} - {self.status}"
class DailyProgress(models.Model):
    date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    summary = models.TextField()
    optional_photo = models.ImageField(upload_to='progress_photos/', blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Daily Progress'

    def __str__(self):
        return f"{self.project.name} - {self.date}"

    def get_absolute_url(self):
        return reverse('progress_detail', kwargs={'pk': self.pk})


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('materials', 'Materials'),
        ('equipment', 'Equipment'),
        ('permits', 'Permits'),
        ('utilities', 'Utilities'),
        ('transportation', 'Transportation'),
        ('supplies', 'Supplies'),
        ('other', 'Other'),
    ]

    date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.project.name} - {self.get_category_display()} - ${self.amount}"

    def get_absolute_url(self):
        return reverse('expense_detail', kwargs={'pk': self.pk})
