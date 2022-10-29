from time import perf_counter
from uuid import uuid4


def factorize(*numbers):
    d = {}
    for number in numbers:
        key = uuid4()
        d[key] = []
        for i in range(1, number + 1):
            if number % i == 0:
                d[key].append(i)
    return tuple(d.values())



if __name__ == "__main__":
    start = perf_counter()
    a, b, c, d  = factorize(99999, 10651060, 10651060, 10651060)
    elapsed = perf_counter() - start
    print(f"Duration(sync): {elapsed}")
    assert a == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert b == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    assert c == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]