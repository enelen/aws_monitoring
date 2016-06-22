import requests
import bs4
import smtplib
import argparse
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class Monitor(object):

    def __init__(self, smtp_server, from_address, to_address):
        self.smtp_server = smtp_server
        self.from_address = from_address
        self.to_address = to_address
        self.result = requests.get('http://status.aws.amazon.com/')
        try:
            self.result.raise_for_status()
        except Exception as exc:
            print('There was a problem during connection: {}'.format(exc))

    def get_status(self):
        # Get HTML source of status page
        soup = bs4.BeautifulSoup(self.result.text, "lxml")
        status = {}
        # Find table that contains list of services
        soup_na = soup.find('div', {'id': 'NA_block'}).tbody
        # Get status of each service
        for tr in soup_na.find_all('tr'):
            service = tr.find('td', {'class': 'bb top pad8'}).text
            state = tr.find('td', {'class': 'bb pad8'}).text
            status[service] = state
        return status

    def send_mail(self, notification_text):
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = 'Monitoring results'
        body = "Next services have a problems:\n" + notification_text
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        try:
            server = smtplib.SMTP(self.smtp_server, timeout=10)
            server.sendmail(self.from_address, self.to_address, text)
            server.quit()
        except Exception as exc:
            print('There was a problem during sending a mail: {}'.format(exc))

    def check_status(self):
        status = self.get_status()
        notifications = []
        #Check status of each service and prepare notification text for email
        for service in status:
            if status[service] != "Service is operating normally":
                notification = '{0} - {1}'.format(service, status[service])
                notifications.append(notification)
        if len(notifications) > 0:
            #Case insensitive sort of notifications
            notifications.sort(key=lambda x: x.lower())
            notification_text = '\n'.join(notifications)
            self.send_mail(notification_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("smtp_server", help="smtp server address")
    parser.add_argument("from_address", help="send mails from this address")
    parser.add_argument("to_address", help="send mails to this address")
    args = parser.parse_args()

    m = Monitor(args.smtp_server, args.from_address, args.to_address)
    m.check_status()
