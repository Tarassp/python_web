from concurrent.futures import ProcessPoolExecutor
from os import cpu_count
from time import perf_counter


def async_factorize(*numbers):
    max_workers = min(cpu_count(), len(numbers))
    with ProcessPoolExecutor(max_workers) as exe:
        results = exe.map(factorize, numbers)
    return results

def factorize(number):
    result = []
    for i in range(1, number + 1):
            if number % i == 0:
                result.append(i)
    return result


if __name__ == "__main__":
    start = perf_counter()
    a, b, c, d  = async_factorize(99999, 10651060, 10651060, 10651060)
    elapsed = perf_counter() - start
    print(f"Duration(sync): {elapsed}")
    assert a == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert b == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    assert c == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]