#!/bin/bash
# PythonAnywhere Deployment Setup Script
# Run this on PythonAnywhere after cloning your repository

echo "🚀 Starting PythonAnywhere Deployment Setup..."

# Step 1: Create virtual environment
echo "📦 Creating virtual environment..."
mkvirtualenv --python=/usr/bin/python3.10 myapp_venv

# Step 2: Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Step 3: Navigate to Django app directory
cd mysite

# Step 4: Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Step 5: Create superuser (optional, commented out)
# python manage.py createsuperuser

# Step 6: Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Step 7: Verify setup
echo "✅ Verifying setup..."
python manage.py check

echo ""
echo "✅ Setup Complete!"
echo ""
echo "⚠️  NEXT STEPS:"
echo "1. Set environment variables in PythonAnywhere Web app settings:"
echo "   - DJANGO_SECRET_KEY (generate a new key)"
echo "   - DJANGO_DEBUG=0"
echo "   - DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com"
echo "   - DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com"
echo "   - DJANGO_FORCE_SSL=1"
echo ""
echo "2. Configure WSGI file to point to: mysite/mysite/wsgi.py"
echo ""
echo "3. Click 'Reload' button in Web app settings"
echo ""
echo "4. Visit https://yourusername.pythonanywhere.com to test"
echo ""

