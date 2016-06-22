#!/bin/ash
postfix start
/usr/bin/python /src/monitor.py ${SMTP_SERVER} ${FROM_ADDRESS} ${TO_ADDRESS}
# Takes some time to send email before exiting container
sleep 10s
