import notifier
import datetime

from ECC import message
from ECC import dataFromMessage

def getTestCase(testNo, length):
	if testNo > 2**length - 1:
		return False

	out = []
	while testNo > 0:
		out.append(testNo % 2)
		testNo //= 2

	while len(out) != length:
		out.append(0)

	return out[::-1]

def testGenerator(finalLength):
	for length in range(1, finalLength+1):
		for n in range(0,2**length):
			print(getTestCase(n, length))

def testMessages(startLength, finalLength):
	for l in range(startLength, finalLength + 1):
		print("Starting", l, datetime.datetime.now())
		for n in range(0, 2**l):
			v = getTestCase(n, l)
			if dataFromMessage(message(v)) != v:
				info = "Test Case: " + n + ", " + l + "\n"
				info += "message: " + str(message(v)) + "\n"
				info += "data back: " + str(dataFromMessage(message(v)))
				notifier.sendError(info)
				return