def main():
    print(check_sum(file="values.txt"))
    # print(check_sum(file="test.txt"))

# First attempt: Valid
# Surely, there are better ways to do this (or, at least, ways to do it with less code).
# Next i might try using more built-in functions to check the numbers on each line of the input.
def check_sum(file=""):
    '''
    First approach to the solution:
        After opening the file (given the input is in a .txt), this function goes through each
        line of it, uses two variables, `begin` and `end`, to parse the string from it's beginning
        and ending until a number is found. These two values are used to compose a two digit number.
        After this, these values are stored in the `lines_sum` list.
        After all the input is used, the return is the sum of all numbers.

    ### Parameters
    `file`: `str`
        The file name or location of the input of the problem.

    ### Returns
    `int`
        An integer representing the sum of all the desired values from the input.
    '''

    try:
        file = open(file=file, mode='r')
    except:
        raise OSError("Error openning file.")

    lines_sum = []
    with file:
        for line in file:
            line_value = ""
            begin = 0
            end = -2 # We start at -2 because line ends with \n

            for _ in range(len(line)):
                first = line[begin]
                if first.isnumeric():
                    line_value += first
                    break
                else:
                    begin += 1

            for _ in range(len(line)-1):
                last = line[end]
                if last.isnumeric():
                    line_value += last
                    break
                else:
                    end -= 1

            lines_sum.append(int(line_value))

    file.close()
    return sum(lines_sum)



if __name__ == '__main__':
    main()
