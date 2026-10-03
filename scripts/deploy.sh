#!/bin/bash

# --- Configuration ---
PROJECT_ROOT="/home/nginx/FishingLog"
VENV_PATH="/home/nginx/FishingLog/.fly_env"
GUNICORN_SERVICE_NAME="gunicorn.service"

# --- Script Execution ---

echo "Starting deployment workflow..."

# 1. Navigate to the project root directory
echo "Navigating to project directory: $PROJECT_ROOT"
cd "$PROJECT_ROOT" || { echo "Error: Could not change to project directory. Exiting."; exit 1; }

# 2. Perform Git pull
echo "Pulling latest changes from Git repository..."
git pull || { echo "Error: Git pull failed. Please resolve conflicts or check connectivity. Exiting."; exit 1; }
echo "Git pull complete."

# 3. Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate" || { echo "Error: Could not activate virtual environment. Exiting."; exit 1; }
echo "Virtual environment activated."

# 4. Install/Update Python dependencies
echo "Installing/updating Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || { echo "Error: pip install failed. Check requirements.txt. Exiting."; deactivate; exit 1; }
elif [ -f "requirments.txt" ]; then
    pip install -r requirments.txt || { echo "Error: pip install failed. Check requirments.txt. Exiting."; deactivate; exit 1; }
fi
echo "Python dependencies updated."

# 5. Run Django database migrations
echo "Running Django database migrations..."
python manage.py migrate || { echo "Error: Django migrations failed. Check database connection/models. Exiting."; deactivate; exit 1; }
echo "Django migrations complete."

# 6. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Error: Django collectstatic failed. Check STATIC_ROOT. Exiting."; deactivate; exit 1; }
echo "Static files collected."

# 7. Deactivate virtual environment
echo "Deactivating virtual environment."
deactivate

# 8. Restart Gunicorn service
echo "Restarting Gunicorn service: $GUNICORN_SERVICE_NAME"
sudo systemctl restart "$GUNICORN_SERVICE_NAME" || { echo "Error: Gunicorn service restart failed. Check service status. Exiting."; exit 1; }
echo "Gunicorn service restarted."

echo "Deployment workflow complete!"
