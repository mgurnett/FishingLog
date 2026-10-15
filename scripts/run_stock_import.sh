#!/bin/bash
# ==============================================================================
# Daily Fish Stocking Import Runner
# ==============================================================================
# This script is meant to be called daily by cron.
# It sets up paths, logs timestamps, downloads the newest PDF report,
# and updates the MariaDB database.
# ==============================================================================

set -e

# Default production paths (falls back to local if /home/nginx does not exist)
if [ -d "/home/nginx/FishingLog" ]; then
    PROJECT_ROOT="/home/nginx/FishingLog"
    VENV_PATH="/home/nginx/FishingLog/.fly_env"
else
    # Fallback to current directory or dev setup
    PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    if [ -d "$PROJECT_ROOT/.fly_env" ]; then
        VENV_PATH="$PROJECT_ROOT/.fly_env"
    elif [ -d "$PROJECT_ROOT/.venv" ]; then
        VENV_PATH="$PROJECT_ROOT/.venv"
    else
        VENV_PATH="$PROJECT_ROOT/venv"
    fi
fi

LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/stock_import.log"

# Create logs directory if it does not exist
mkdir -p "$LOG_DIR"

echo "======================================================================" >> "$LOG_FILE"
echo "🎣 Daily Fish Stocking Import Started at $(date)" >> "$LOG_FILE"
echo "Working directory: $PROJECT_ROOT" >> "$LOG_FILE"
echo "======================================================================" >> "$LOG_FILE"

cd "$PROJECT_ROOT"

# Ensure poppler-utils (pdftotext) is available
if ! command -v pdftotext &> /dev/null; then
    echo "⚠️ Warning: 'pdftotext' not found in PATH. Make sure 'poppler-utils' is installed." >> "$LOG_FILE"
fi

# Execute stocking import with --force-download to get fresh PDF data daily
"$VENV_PATH/bin/python" scripts/pdf_to_db_stockings.py --force-download >> "$LOG_FILE" 2>&1

echo "" >> "$LOG_FILE"
echo "✅ Import finished at $(date)" >> "$LOG_FILE"
echo "======================================================================" >> "$LOG_FILE"
