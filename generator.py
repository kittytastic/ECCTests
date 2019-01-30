import notifier
import datetime
import random

from answers import message
from answers import dataFromMessage
from answers import hammingEncoder
from answers import hammingDecoder
from answers import messageFromCodeword


import advanced_test

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

def fullHammingTest(v):
	m = message(v)
	encoded = hammingEncoder(m)

	noise = advanced_test.random_noise(encoded, random.randint(0,1))

	decoded = hammingDecoder(noise)
	recoveredMessage = messageFromCodeword(decoded)
	recoveredData = dataFromMessage(recoveredMessage)

	assert v == recoveredData,{"recoverable": True,
	 "v": v,
	 "message": m,
	 "encoded": encoded,
	 "noise": noise,
	 "decoded": decoded,
	 "recoveredMessage": recoveredMessage,
	 "recoveredData": recoveredData
	}

	#Not recoverable
	noise = advanced_test.random_noise(encoded, 2)
	decoded = hammingDecoder(noise)

	assert decoded == [], {"recoverable": False,
	 "v": v,
	 "encoded": encoded,
	 "noise": noise,
	 "decoded": decoded
	}

def runTests(start, end):
	for l in range(start, end):
		for n in range(0, 2**l):
			v = getTestCase(n, l)
			try:
				fullHammingTest(v)
			except AssertionError as e:
				info = ""
				for key, val in e.args[0].items():
					info += key + ": " + str(val) + "\n"
				notifier.addError(info)
				notifier.sendErrors()

runTests(1,2)