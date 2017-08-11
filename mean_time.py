import sys

file = sys.argv[1]
file_cursor = open(file)
file_content = [line for line in file_cursor.readlines() if len(line) > 1]
realtimes = [line for (index, line) in enumerate(file_content) if index % 3 == 0]

float_times = []
for time_line in realtimes:
    time_line = time_line.replace("real\t", "").replace("0m", "").replace("s", "").replace("\n", "")
    float_times.append(float(time_line))

average_time = sum(float_times) / len(float_times)

print("Average time:", average_time)