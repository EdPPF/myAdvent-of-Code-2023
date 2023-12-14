def main():
    # print(check_sum(file="values.txt"))
    # print(check_sum(file="test.txt"))

    # print(check_sum2('values.txt'))

    print(third_impact('values.txt'))

    import timeit
    timeit.timeit(check_sum(file='../values.txt'), number=10000)
    timeit.timeit(check_sum2(file='../values.txt'), number=10000)
    timeit.timeit(third_impact(file='../values.txt'), number=10000)

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

# Second attempt: Valid
# While this works and is more concise, it is more restrained than the first solution.
# One drawback i can see is that it only works if the string contains what is specified in `n`.
# Because of that, i still prefer the first attempt.
def check_sum2(file='') -> int:
    '''
    Second approach to the solution:
        Using the same idea of `check_sum`, this function uses the `strip` function to
        remove non digits from each line of the input while composing the two digit number.

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

    values = []
    for line in file.readlines():
        n = "abcdefghijklmnopqrstuvwxyz\n"
        first = line.strip(n)[0]
        last = line.strip(n)[-1]
        values.append(int(first+last))

    file.close()

    return sum(values)

# Third attempt: Valid
# Oh well. This one is way simpler than the other two.
# It uses list comprehension, which is something i should've used in the first place.
def third_impact(file='') -> int:
    '''
    Third approach to the solution:
        This function uses the `isdigit` function with list comprehension to check if a
        character is a digit. If so, it is added to a list. After all the input is used,
        the return is the sum of all numbers.

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

    values = []
    for line in file:
        digits = [char for char in line if char.isdigit()]
        values.append(int(digits[0]+digits[-1]))

    file.close()

    return sum(values)


if __name__ == '__main__':
    main()
