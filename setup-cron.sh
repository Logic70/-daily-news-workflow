#!/bin/bash
# Daily News Cron Setup Script
# Usage: ./setup-cron.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_LINE="0 9 * * * cd $SCRIPT_DIR && $SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/scripts/fetch-news.py --output $SCRIPT_DIR/cache/daily-\$(date +\\%Y-\\%m-\\%d).json && $SCRIPT_DIR/venv/bin/python $SCRIPT_DIR/scripts/generate-pdf.py --input $SCRIPT_DIR/cache/daily-\$(date +\\%Y-\\%m-\\%d).json --output $SCRIPT_DIR/output/tech-news-digest-\$(date +\\%Y-\\%m-\\%d).pdf >> $SCRIPT_DIR/logs/cron.log 2>&1"

echo "=== Daily News Cron Setup ==="
echo ""
echo "This will add the following cron job:"
echo "  Time: Daily at 09:00"
echo "  Command: $CRON_LINE"
echo ""
read -p "Add to crontab? (y/n): " confirm

if [[ $confirm == [yY] ]]; then
    # Ensure logs directory exists
    mkdir -p "$SCRIPT_DIR/logs"

    # Export env vars for cron
    echo "export NEWS_API_KEY='$NEWS_API_KEY'" > "$SCRIPT_DIR/.env.cron"

    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

    echo ""
    echo "✓ Cron job added successfully!"
    echo ""
    echo "Current crontab:"
    crontab -l
else
    echo "Cancelled."
fi
