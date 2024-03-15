from src.solution import *
import time

times = []
for i in range(3):
    start = time.perf_counter()
    result = second_impact("./input.txt")
    end = time.perf_counter()
    elapsed_time = end - start
    print(f"....Test {i+1}: {elapsed_time:.3f} seconds")
    times.append(elapsed_time)
average = sum(times)/3.0
print(f"RESULT = {result} - Average time: {average:.3f} seconds")
