def main():
    print(check_sum(file="values.txt"))
    # print(check_sum(file="test.txt"))

# First attempt:
# Surely, there are better ways to do this (or, at least, ways to do it eith less code).
# Next i might try using more built-in functions to check the numbers on each line of the input.
def check_sum(file=""):
    if (file == ""):
        return "File unreachable, please check if the file exists or is in the correct location."

    lines_sum = []
    file = open(file=file, mode="r")
    for line in file:
        line_value = ""
        begin = 0
        end = -2 # We start at -2 because line ends with \n

        for i in range(len(line)):
            first = line[begin]
            if first.isnumeric():
                line_value += first
                break
            else:
                begin += 1

        for j in range(len(line)-1):
            last = line[end]
            if last.isnumeric():
                line_value += last
                break
            else:
                end -= 1

        lines_sum.append(int(line_value))

    return sum(lines_sum)



if __name__ == '__main__':
    main()
