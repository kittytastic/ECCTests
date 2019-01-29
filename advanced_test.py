import sys
import random

from qwrx21 import repetitionEncoder
from qwrx21 import repetitionDecoder


def randomNoice(m, bits_to_flip):

    message_len = len(m)

    seen_pos = []

    flipped_count = 0

    if bits_to_flip>message_len:
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


def test():
    assert repetitionEncoder([0], 4) == [0, 0, 0, 0]
    assert repetitionEncoder([1], 5) == [1, 1, 1, 1, 1]

    assert repetitionDecoder([1, 1, 1, 1]) == [1]
    assert repetitionDecoder([1, 1, 1, 1, 1]) == [1]
    assert repetitionDecoder([1, 1, 0, 0]) == []
    assert repetitionDecoder([1, 1, 0, 0, 0]) == [0]
    assert repetitionDecoder([0, 0, 0, 0]) == [0]
    assert repetitionDecoder([1, 0, 0, 0]) == [0]
    assert repetitionDecoder([1, 1, 1, 0]) == [1]

    # Test that repetition codes can encode and decode message WITHOUT interference
    for i in range(100):
        original_mes = [random.randint(0, 1)]
        encoded = repetitionEncoder(original_mes, random.randint(2, 20))
        decoded = repetitionDecoder(encoded)

        #print("Orig: %s   Enc: %s   Dec: %s"%(original_mes,encoded,decoded))
        assert original_mes == decoded

    # Test that repetition codes can encode and decode message WITHOUT interference
    for i in range(100):
        original_mes = [random.randint(0, 1)]
        code_len = random.randint(2, 5)
        error_bits = random.randint(1, code_len//2)

        encoded = repetitionEncoder(original_mes, code_len)
        scrambled = randomNoice(encoded,error_bits)
        decoded = repetitionDecoder(scrambled)

        expected = original_mes

        if (code_len%2) == 0:
            if error_bits == code_len//2:
                expected = []


        print("Orig: %s   Enc: %s   Dec: %s   Exp: %s"%(original_mes,encoded,decoded,expected))
        assert decoded == expected

    print("Passed repetition Tests")

for i in range(10):
    k = [1]*5
    print(randomNoice(k, 2))

#test()