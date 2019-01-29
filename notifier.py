import smtplib
import config

def send_email(subject, msg):
	try:
		server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

		server.login(config.loginInfo["username"], config.loginInfo["password"])

		message = "Subject: {} \n\n{}".format(subject, msg)

		server.sendmail(config.loginInfo["username"], config.sendTo, message)
		server.quit()
	except Exception as e:
		print("Message Failed to send")
