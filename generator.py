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