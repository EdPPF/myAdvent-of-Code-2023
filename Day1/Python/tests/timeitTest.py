import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from solution import *
import timeit

def test_time_check_sum():
    start_time = timeit.default_timer()
    check_sum(file='values.txt')
    end_time = timeit.default_timer()
    print(f"Time taken for check_sum: \n{end_time - start_time} seconds")

def test_time_check_sum2():
    start_time = timeit.default_timer()
    check_sum2(file='values.txt')
    end_time = timeit.default_timer()
    print(f"Time taken for check_sum2: \n{end_time - start_time} seconds")

def test_time_third_impact():
    start_time = timeit.default_timer()
    third_impact(file='values.txt')
    end_time = timeit.default_timer()
    print(f"Time taken for third_impact: \n{end_time - start_time} seconds")

def test_time_check_real_sum():
    start_time = timeit.default_timer()
    check_real_sum(file='values.txt')
    end_time = timeit.default_timer()
    print(f"Time taken for check_real_sum: \n{end_time - start_time} seconds")

def test_time_second_alg():
    start_time = timeit.default_timer()
    second_alg('values.txt')
    end_time = timeit.default_timer()
    print(f"Time taken for second_alg: \n{end_time - start_time} seconds")

if __name__ == "__main__":
    test_time_check_sum()
    print("---")
    test_time_check_sum2()
    print("---")
    test_time_third_impact()
    print("---")
    test_time_check_real_sum()
    print("---")
    test_time_second_alg()
    print("---")
