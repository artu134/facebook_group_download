#!/bin/bash

# Path to the Python script
SCRIPT="./main_weekly.py"


# Add cron job to crontab
(crontab -l 2>/dev/null; echo "0 0 * * 0 python $SCRIPT >> $LOG 2>&1") | crontab -
