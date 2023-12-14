import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from solution import check_sum, check_sum2, third_impact
import timeit

def test_time_function1():
    start_time = timeit.default_timer()
    check_sum(file='values.txt')
    end_time = timeit.default_timer()
    print(f"Time taken for check_sum: {end_time - start_time} seconds")

def test_time_function2():
    start_time = timeit.default_timer()
    check_sum2(file='values.txt')
    end_time = timeit.default_timer()
    print(f"Time taken for check_sum2: {end_time - start_time} seconds")

def test_time_function3():
    start_time = timeit.default_timer()
    third_impact(file='values.txt')
    end_time = timeit.default_timer()
    print(f"Time taken for third_impact: {end_time - start_time} seconds")

if __name__ == "__main__":
    test_time_function1()
    test_time_function2()
    test_time_function3()
