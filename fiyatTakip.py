import smtplib
import ssl

import datetime as dt
import time
import locale

from bs4 import BeautifulSoup
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

locale.setlocale(locale.LC_ALL, '')


def chech_price():
    page = requests.get("https://www.trendyol.com/stradivarius/cikarilabilir-kapusonlu-su-gecirmez-mont-p-144434979?v=m")
    source = BeautifulSoup(page.content, 'lxml')
    price = source.find("span", attrs={"class": "prc-dsc"}).text
    price = price.replace(",", ".").split()[0]
    return price


def send_mail(subject, mesaj, my_mail_address, password, send_to):

    message = MIMEMultipart()
    message["From"] = my_mail_address
    message["To"] = send_to
    message["Subject"] = subject
    message["Bcc"] = send_to
    message.attach(MIMEText(mesaj, "plain"))
    yazi = message.as_string()
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.yandex.com.tr", 465, context=context) as server:
        server.login(my_mail_address, password)
        server.sendmail(my_mail_address, send_to, yazi.encode("utf-8"))
        server.quit()


prev_price = chech_price()

first_email_time = dt.datetime.now() + dt.timedelta(minutes=1)
interval = dt.timedelta(minutes=10)  # set the interval for sending the email

send_time = first_email_time

sent = False
while not sent:
    time.sleep(send_time.timestamp() - time.time())
    price = chech_price()
    print("kontrol")
    if int(float(price)) != int(float(prev_price)):
        icerik = "Eski fiyat: " + prev_price + " Yeni Fiyat: " + price
        send_mail("Fiyat Değişikliği", icerik, "gönderici mail", "sifre",
                  "alıcı mail")
        print("bitti")
        sent = True
    else:
        send_time = send_time + interval
