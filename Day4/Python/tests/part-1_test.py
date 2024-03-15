from src import first_impact
import time

print("---- TESTING PART 1 ----")

print("Valid for test input:", first_impact("./test.txt") == 13)
print("Valid for real input:", first_impact("./input.txt") == 26218)

times = []
for i in range(3):
    start = time.perf_counter()
    result = first_impact("./input.txt")
    end = time.perf_counter()
    elapsed_time = end - start
    print(f"....Test {i+1}: {elapsed_time:.3f} seconds")
    times.append(elapsed_time)
average = sum(times)/3.0
print(f"RESULT = {result} - Average time: {average:.3f} seconds")
