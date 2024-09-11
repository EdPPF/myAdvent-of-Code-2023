from src import first_impact
import time, unittest

class TestFirstImpact(unittest.TestCase):
    def test_first_impact(self):
        print("---- TESTING PART 1 ----")
        self.assertEqual(first_impact("./test.txt"),  PUT_RESULT_HERE)
        self.assertEqual(first_impact("./input.txt"), PUT_RESULT_HERE)

        times = []
        for i in range(3):
            start = time.perf_counter()
            result = first_impact("./input.txt")
            end = time.perf_counter()
            elapsed_time = end - start
            print(f"....Test {i+1}: {elapsed_time:.3f} seconds")
            times.append(elapsed_time)
        average = sum(times)/3.0
        print(f"RESULT = {result} - Average time: {average:3f} seconds")
