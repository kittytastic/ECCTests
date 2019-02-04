import notifier
import datetime
import random
import copy
import math


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


def checkMessageLength(m, v):
	r = math.ceil(math.log(len(m), 2))

	while 2**r - r -1 > len(m):
		r -= 1

	while 2**r - r -1 < len(m):
		r += 1

	if r < 2:
		r = 2

	assert 2**r - r - 1 == len(m), {"Test": "checkMessageLength",
	"v": v,
	"m": m,
	"length": len(m),
	"r": r} 

def checkHammingEncoderLength(c, v):
	assert math.log(len(c) + 1, 2) % 1 == 0, {"Test": "checkHammingEncoderLength",
	"v": v,
	"c": c,
	"length": len(c)}

def checkHammingDecoderLength(c, v):
	assert math.log(len(c) + 1, 2) % 1 == 0, {"Test": "checkHammingDecoderLength",
	"v": v,
	"c": c,
	"length": len(c)}

def checkMessageFromCodewordLength(m, v):
	r = math.ceil(math.log(len(m), 2))

	while 2**r - r -1 > len(m):
		r -= 1

	while 2**r - r -1 < len(m):
		r += 1

	if r < 2:
		r = 2

	assert 2**r - r - 1 == len(m), {"Test": "checkMessageFromCodewordLength",
	"v": v,
	"m": m,
	"length": len(m),
	"length it should be": 2**r - r - 1,
	"r": r}

def checkVectorIsOnly01(c, v, test):
	for i in v:
		assert i == 0 or i == 1, {"Test": "checkVectorIsOnly01 following " + test,
		"v": v,
		"c": c}

def fullHammingTest(v):
	m = message(v)
	checkVectorIsOnly01(m, v, "message")
	checkMessageLength(m, v)

	encoded = hammingEncoder(copy.copy(m))
	checkVectorIsOnly01(encoded, v, "hammingEncoder")
	checkHammingEncoderLength(encoded, v)

	decoded = hammingDecoder(copy.copy(encoded))
	checkVectorIsOnly01(decoded, v, "hammingDecoder")
	checkHammingDecoderLength(decoded, v)

	recoveredMessage = messageFromCodeword(copy.copy(decoded))
	checkVectorIsOnly01(recoveredMessage, v, "messageFromCodeword")
	checkMessageFromCodewordLength(recoveredMessage, v)

	recoveredData = dataFromMessage(copy.copy(recoveredMessage))
	checkVectorIsOnly01(recoveredData, v, "dataFromMessage")

	assert v == recoveredData, {"Test": "comprehensiveHammingTest no noise",
	 "v": v,
	 "message": m,
	 "encoded": encoded,
	 "decoded": decoded,
	 "recoveredMessage": recoveredMessage,
	 "recoveredData": recoveredData
	}

	noise = advanced_test.random_noise(copy.copy(encoded), 1)

	decoded = hammingDecoder(copy.copy(noise))
	checkVectorIsOnly01(decoded, v, "hammingDecoder")
	checkHammingDecoderLength(decoded, v)

	recoveredMessage = messageFromCodeword(copy.copy(decoded))
	checkVectorIsOnly01(recoveredMessage, v, "messageFromCodeword")
	checkMessageFromCodewordLength(recoveredMessage, v)

	recoveredData = dataFromMessage(copy.copy(recoveredMessage))
	checkVectorIsOnly01(recoveredData, v, "dataFromMessage")

	assert v == recoveredData, {"Test": "comprehensiveHammingTest with noise",
	 "v": v,
	 "message": m,
	 "encoded": encoded,
	 "noise": noise,
	 "decoded": decoded,
	 "recoveredMessage": recoveredMessage,
	 "recoveredData": recoveredData
	}


def runTests(start, end):
	for l in range(start, end + 1):
		print("starting", l)
		for n in range(0, 2**l):
			v = getTestCase(n, l)
			try:
				fullHammingTest(v)
			except AssertionError as e:
				info = ""
				for key, val in e.args[0].items():
					info += key + ": " + str(val) + "\n"
				print(info)
				notifier.addError(info)
				notifier.sendErrors()