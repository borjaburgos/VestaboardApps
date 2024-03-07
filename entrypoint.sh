#!/bin/bash
printenv > /etc/environment

# Start cron in the foreground
cron -f &

# Display logs
tail -f /var/log/cron.log