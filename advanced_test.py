import sys
import random

from answers import repetitionEncoder
from answers import repetitionDecoder
from answers import message
from answers import dataFromMessage

from answers import hammingEncoder
from answers import hammingDecoder
from answers import messageFromCodeword


def random_noise(m, bits_to_flip):

    message_len = len(m)
    seen_pos = []
    flipped_count = 0

    if bits_to_flip > message_len:
        sys.exit("Cannot flip more bits than there are bits in the message")

    while flipped_count < bits_to_flip:

        pos = random.randint(0, message_len-1)
        if not (pos in seen_pos):
            seen_pos.append(pos)
            m[pos] = flip_bit(m[pos])
            flipped_count += 1

    return m


def flip_bit(bit):
    if bit == 0:
        return 1
    if bit == 1:
        return 0
    else:
        sys.exit("Flipping bit that isn't 0 or 1")


def random_message(length):
    m = []
    for i in range(length):
        m.append(random.randint(0, 1))
    return m


def hard_coded_tests():
    m = "Failed to encode to repetition code"
    assert repetitionEncoder([0], 4) == [0, 0, 0, 0], m
    assert repetitionEncoder([1], 5) == [1, 1, 1, 1, 1], m

    m = "Failed to decode repetition code"
    assert repetitionDecoder([1, 1, 1, 1]) == [1], m
    assert repetitionDecoder([1, 1, 1, 1, 1]) == [1], m
    assert repetitionDecoder([1, 1, 0, 0]) == [], m
    assert repetitionDecoder([1, 1, 0, 0, 0]) == [0], m
    assert repetitionDecoder([0, 0, 0, 0]) == [0], m
    assert repetitionDecoder([1, 0, 0, 0]) == [0], m
    assert repetitionDecoder([1, 1, 1, 0]) == [1], m

    # All from questions
    m = "Failed correctly encode message to data"
    assert message([1]) == [0, 0, 1, 1], m
    assert message([0, 0, 1]) == [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0], m
    assert message([0, 1, 1, 0]) == [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0], m
    assert message([1, 1, 1, 1, 0, 1]) == [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0], m
    assert message([0, 1, 1, 0, 1]) == [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0], m

    # All from questions
    assert dataFromMessage([1, 0, 0, 1, 0, 1, 1, 0, 1, 0]) == [], "Failed to spot error when getting data from message when message is too short"
    assert dataFromMessage([1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0]) == [], "Failed to spot error when getting data from message when l>number of bits in message"
    assert dataFromMessage([0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0]) == [0, 1, 1, 0, 1], "Failed to get correct data from message"

    assert hammingEncoder([1, 1, 1]) == [], "Failed to return error encoding messages of incorrect length"
    assert hammingEncoder([1, 0, 0, 0]) == [1, 1, 1, 0, 0, 0, 0], "Failed to hamming encode correctly"


# Encode a message using repetition code then decodes it
# Checks: repetitionEncoder(), repetitionDecoder()
def test_rep_encode_decode():
    original_mes = [random.randint(0, 1)]
    encoded = repetitionEncoder(original_mes, random.randint(2, 20))
    decoded = repetitionDecoder(encoded)

    assert original_mes == decoded, "Repetition code failed to get encoded then immediately decoded"


# Encode a message using repetition code applies random noise then decodes it
def test_rep_encode_noise_decode():
    original_mes = [random.randint(0, 1)]
    code_len = random.randint(2, 5)
    error_bits = random.randint(1, code_len // 2)
    encoded = repetitionEncoder(original_mes, code_len)
    scrambled = random_noise(encoded, error_bits)
    decoded = repetitionDecoder(scrambled)
    expected = original_mes

    if (code_len % 2) == 0:
        if error_bits == code_len // 2:
            expected = []

    assert decoded == expected, "Repetition code failed to decode correctly"


# Check message() returns messages of correct length
def test_message_length():
    # max message length 100
    original = random_message(random.randint(1,100))
    length = len(message(original))

    r = 2
    l = 2**r - 2*r - 1
    while l < length:
        r += 1
        l = 2 ** r - r - 1

    assert l == length, "Message failed to encode to an expected length"


# Encodes a message then immediately decode it
# Checks basic functionality for: message(), dataFromMessage()
def test_message_encode_decode():
    original = random_message(random.randint(1,100))
    mes = message(original)
    decode = dataFromMessage(mes)

    assert decode == original, "Message failed to get encoded and decoded (no hamming codes) without changing"


def test_full_ham_encode_cycle():
    original = random_message(random.randint(1, 100))
    mess = message(original)
    encoded = hammingEncoder(mess)
    code_word = hammingDecoder(encoded)
    mess = messageFromCodeword(code_word)
    end_data = dataFromMessage(mess)

    assert original == end_data, "Encoded message but when decoded didn't get same answer %s  %s"%(original,end_data)

def test_full_ham_cycle_noise():
    original = random_message(random.randint(1, 1000))
    mess = message(original)
    encoded = hammingEncoder(mess)
    dirty = random_noise(encoded, 1)
    code_word = hammingDecoder(dirty)
    mess = messageFromCodeword(code_word)
    end_data = dataFromMessage(mess)

    assert original == end_data, "Encoded message but when decoded didn't get same answer %s  %s"%(original,end_data)



def test():
    # Do all manually generated tests
    print("Trying all hardcoded tests")
    hard_coded_tests()
    print("    - Passed")

    # Test repetition code
    print("Trying repetition code tests")
    for i in range(10000):
        test_rep_encode_decode()
        test_rep_encode_noise_decode()
    print("    - Passed")

    print("Trying message only tests")
    for i in range(10000):
        pass
        #test_message_length()
        #test_message_encode_decode()

    print("    - Passed")

    print("Trying full hamming cycle tests")
    for i in range(10000):
        test_full_ham_encode_cycle()
        test_full_ham_cycle_noise()
        if i % 100 == 0:
            print("%d %%"%(i//100))
    print("    - Passed")


    print("All tests passed")


print("---------------------- Advanced tester ----------------------")
test()
