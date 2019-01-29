import smtplib
import config

errorLog = []

def send_email(subject, msg):
	try:
		server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

		server.login(config.loginInfo["username"], config.loginInfo["password"])

		message = "Subject: {} \n\n{}".format(subject, msg)

		server.sendmail(config.loginInfo["username"], config.sendTo, message)
		server.quit()
	except Exception as e:
		print("Message Failed to send")

def sendUpdate(currentTestCase):
	send_email("Update: " + currentTestCase, 
		"Testing is still running and is on " + currentTestCase + ".")

## Instead of sending every error one at a time send them in bulk
## so you don't get a steady flow of 100s of emails when something goes wrong.
def addError(errorInfo):
	errorLog.append(errorInfo)

def sendErrors():
	message = "\n\n\n".join(errorLog)
	send_email("Errors: " + len(errorLog), message)

def sendError(errorInfo):
	send_email("Error", errorInfo)