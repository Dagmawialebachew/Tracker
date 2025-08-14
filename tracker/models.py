from django.db import models
from django.urls import reverse
from decimal import Decimal


class Project(models.Model):
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
        """Calculate total labor cost for this project"""
        total = Decimal('0.00')
        for laborer in self.laborer_set.all():
            # Calculate days between start and end date
            days = (self.end_date - self.start_date).days + 1
            total += laborer.daily_rate * days
        return total
    
    @property
    def total_expenses(self):
        """Calculate total expenses for this project"""
        return sum(expense.amount for expense in self.expense_set.all())
    
    @property
    def progress_count(self):
        """Count of daily progress entries"""
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