# Construction Project Tracker

A comprehensive Django web application designed for construction and contractor businesses to track projects, manage laborers, monitor daily progress, and control expenses.

## Features

### Core Functionality
- **Project Management**: Create, edit, and track construction projects with timelines
- **Workforce Management**: Assign laborers with roles and daily rates to projects  
- **Progress Tracking**: Log daily progress updates with optional photo uploads
- **Expense Control**: Track and categorize project expenses with detailed reporting
- **Financial Reporting**: Generate comprehensive project reports with cost breakdowns

### Technical Features
- **Mobile-Responsive Design**: Optimized for tablets and phones used on construction sites
- **Professional UI**: Clean, construction-themed interface using Tailwind CSS
- **Dashboard Analytics**: Overview statistics and recent activity summaries
- **Image Uploads**: Support for progress photos with proper media handling
- **Data Validation**: Comprehensive form validation and error handling

## Models

### Project
- Name, location, start date, end date
- Calculated properties for total labor cost and expenses
- Automatic project timeline and progress tracking

### Laborer  
- Name, role (foreman, electrician, plumber, etc.), daily rate
- Assignment to specific projects
- Role-based categorization for reporting

### Daily Progress
- Date-based progress entries tied to projects
- Text summaries with optional photo uploads
- Timeline tracking for project history

### Expense
- Categorized expenses (materials, equipment, permits, utilities, etc.)
- Project-specific cost tracking
- Notes and amount tracking with decimal precision

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 4.x
- Pillow (for image handling)

### Installation

1. **Install Dependencies**
```bash
pip install Django Pillow
```

2. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Load Sample Data (Optional)**
```bash
python manage.py load_sample_data
```

4. **Create Admin User (Optional)**
```bash
python manage.py createsuperuser
```

5. **Run Development Server**
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Sample Data

The application includes a management command to load realistic demo data:
- 3 sample construction projects (residential, commercial, retail)
- 8 laborers with different roles and realistic rates
- 5 progress updates with construction-specific summaries  
- 9 expense entries across different categories

## Usage

### Dashboard
- Overview of all projects with key metrics
- Quick access to recent progress updates and expenses
- Fast creation buttons for common tasks

### Project Management
- Create projects with location and timeline details
- View detailed project pages with assigned workers and progress
- Generate comprehensive financial reports
- Track project timeline and completion status

### Labor Management  
- Add laborers with specific roles and daily rates
- Assign workers to projects for cost calculation
- View labor costs and productivity metrics

### Progress Tracking
- Daily progress entries with rich text descriptions
- Optional photo uploads for visual progress documentation
- Timeline view of project development

### Expense Tracking
- Categorized expense entry (materials, equipment, permits, etc.)
- Project-specific cost allocation
- Summary reporting and cost analysis

## Design

- **Mobile-First**: Responsive design optimized for field use on tablets and phones
- **Professional Theme**: Construction-focused color scheme with orange primary, blue secondary
- **Accessibility**: High contrast text and large touch targets for outdoor visibility
- **Clean Interface**: Card-based layouts with clear visual hierarchy
- **Fast Navigation**: Intuitive menu structure with contextual actions

## File Structure

```
construction_tracker/
├── tracker/                 # Main Django app
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin interface
│   └── management/         # Custom commands
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── tracker/           # App-specific templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploads
└── README.md              # This file
```

## Customization

The application is designed to be easily customizable:

- **Add New Roles**: Modify the `ROLE_CHOICES` in `models.py`
- **Expense Categories**: Update `CATEGORY_CHOICES` for different expense types  
- **Styling**: Customize Tailwind CSS classes in templates
- **Business Logic**: Extend models with additional calculated properties
- **Reporting**: Add new report views and templates

## Production Deployment

For production use:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure media file storage
5. Set up proper logging
6. Use environment variables for sensitive settings

## License

Open source - suitable for commercial use by construction businesses.