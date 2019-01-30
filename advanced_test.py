import sys
import random

from answers import repetitionEncoder
from answers import repetitionDecoder
from answers import message


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
    assert repetitionEncoder([0], 4) == [0, 0, 0, 0]
    assert repetitionEncoder([1], 5) == [1, 1, 1, 1, 1]

    assert repetitionDecoder([1, 1, 1, 1]) == [1]
    assert repetitionDecoder([1, 1, 1, 1, 1]) == [1]
    assert repetitionDecoder([1, 1, 0, 0]) == []
    assert repetitionDecoder([1, 1, 0, 0, 0]) == [0]
    assert repetitionDecoder([0, 0, 0, 0]) == [0]
    assert repetitionDecoder([1, 0, 0, 0]) == [0]
    assert repetitionDecoder([1, 1, 1, 0]) == [1]

    assert message([1]) == [0, 0, 1, 1]
    assert message([0, 0, 1]) == [0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0]
    assert message([0, 1, 1, 0]) == [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    assert message([1, 1, 1, 1, 0, 1]) == [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0]
    assert message([0, 1, 1, 0, 1]) == [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0]


# Encode a message using repetition code then decodes it
def test_rep_encode_decode():
    original_mes = [random.randint(0, 1)]
    encoded = repetitionEncoder(original_mes, random.randint(2, 20))
    decoded = repetitionDecoder(encoded)

    assert original_mes == decoded


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

    assert decoded == expected


# Check messages are of an expected length
def test_message_length():
    # max message length 100
    original = random_message(random.randint(1,100))
    length = len(message(original))

    r = 2
    l = 2**r - 2*r - 1
    while l < length:
        r += 1
        l = 2 ** r - r - 1

    assert l == length


def test():
    # Do all manually generated tests
    print("Trying all hardcoded tests")
    hard_coded_tests()
    print("    - Passed")

    # Test repetition code
    print("Trying auto generated repetition code tests")
    for i in range(10000):
        test_rep_encode_decode()
        test_rep_encode_noise_decode()
    print("    - Passed")

    print("Trying auto generated message only tests")
    for i in range(10000):
        test_message_length()

    print("    - Passed")


    print("All tests passed")


print("---------------------- Advanced tester ----------------------")
test()
