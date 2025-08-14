from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from tracker.models import Project, Laborer, DailyProgress, Expense


class Command(BaseCommand):
    help = 'Load sample data for demonstration'

    def handle(self, *args, **options):
        # Clear existing data
        Project.objects.all().delete()
        
        # Create sample projects
        project1 = Project.objects.create(
            name="Residential Home Construction",
            location="123 Oak Street, Springfield",
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=60)
        )
        
        project2 = Project.objects.create(
            name="Office Building Renovation",
            location="456 Business Park Dr, Downtown",
            start_date=date.today() - timedelta(days=45),
            end_date=date.today() + timedelta(days=30)
        )
        
        project3 = Project.objects.create(
            name="Shopping Center Expansion",
            location="789 Commerce Blvd, Westside",
            start_date=date.today() - timedelta(days=15),
            end_date=date.today() + timedelta(days=90)
        )
        
        # Create sample laborers
        laborers_data = [
            {"name": "John Smith", "role": "foreman", "rate": "350.00", "project": project1},
            {"name": "Mike Johnson", "role": "carpenter", "rate": "280.00", "project": project1},
            {"name": "Sarah Wilson", "role": "electrician", "rate": "320.00", "project": project1},
            {"name": "David Brown", "role": "plumber", "rate": "300.00", "project": project2},
            {"name": "Lisa Davis", "role": "mason", "rate": "270.00", "project": project2},
            {"name": "Tom Anderson", "role": "painter", "rate": "240.00", "project": project2},
            {"name": "Jennifer Martinez", "role": "operator", "rate": "330.00", "project": project3},
            {"name": "Robert Taylor", "role": "general", "rate": "220.00", "project": project3},
        ]
        
        for laborer_data in laborers_data:
            Laborer.objects.create(
                name=laborer_data["name"],
                role=laborer_data["role"],
                daily_rate=Decimal(laborer_data["rate"]),
                assigned_project=laborer_data["project"]
            )
        
        # Create sample progress entries
        progress_data = [
            {
                "project": project1,
                "date": date.today() - timedelta(days=5),
                "summary": "Foundation concrete poured and curing well. Weather conditions have been favorable for the concrete work. All rebar inspections passed."
            },
            {
                "project": project1,
                "date": date.today() - timedelta(days=3),
                "summary": "Framing for first floor completed. Electrical rough-in has begun. Plumbing contractor scheduled for next week."
            },
            {
                "project": project2,
                "date": date.today() - timedelta(days=4),
                "summary": "Demolished old office partitions. Discovered some asbestos tiles that need professional removal before continuing."
            },
            {
                "project": project2,
                "date": date.today() - timedelta(days=1),
                "summary": "Asbestos remediation completed. New electrical conduit installation in progress. HVAC contractor on site tomorrow."
            },
            {
                "project": project3,
                "date": date.today() - timedelta(days=2),
                "summary": "Site preparation complete. Excavation for new foundation started. Utility relocation proceeding on schedule."
            },
        ]
        
        for progress in progress_data:
            DailyProgress.objects.create(**progress)
        
        # Create sample expenses
        expenses_data = [
            {"project": project1, "category": "materials", "amount": "15750.00", "notes": "Lumber delivery - premium grade 2x4, 2x6, plywood", "days_ago": 7},
            {"project": project1, "category": "equipment", "amount": "850.00", "notes": "Concrete mixer rental - 3 days", "days_ago": 5},
            {"project": project1, "category": "supplies", "amount": "420.00", "notes": "Nails, screws, construction adhesive", "days_ago": 4},
            {"project": project2, "category": "permits", "amount": "1200.00", "notes": "Building permit and electrical permit fees", "days_ago": 10},
            {"project": project2, "category": "materials", "amount": "8500.00", "notes": "Drywall, insulation, ceiling tiles", "days_ago": 6},
            {"project": project2, "category": "other", "amount": "2500.00", "notes": "Asbestos removal by certified contractor", "days_ago": 3},
            {"project": project3, "category": "equipment", "amount": "3200.00", "notes": "Excavator rental - 1 week", "days_ago": 8},
            {"project": project3, "category": "utilities", "amount": "750.00", "notes": "Temporary power connection setup", "days_ago": 6},
            {"project": project3, "category": "transportation", "amount": "320.00", "notes": "Material delivery charges", "days_ago": 2},
        ]
        
        for expense_data in expenses_data:
            Expense.objects.create(
                project=expense_data["project"],
                category=expense_data["category"],
                amount=Decimal(expense_data["amount"]),
                notes=expense_data["notes"],
                date=date.today() - timedelta(days=expense_data["days_ago"])
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data with 3 projects, 8 laborers, 5 progress entries, and 9 expenses')
        )