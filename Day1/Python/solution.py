def main():
    # print(check_sum(file="values.txt"))
    # print(check_sum2('values.txt'))
    # print(third_impact('values.txt'))

    # print(check_real_sum('test2.txt'))
    # print(check_real_sum2('test2.txt'))
    print(second_alg('values.txt'))


# Auxiliar function for opening files.
def open_file(path=""):
    try:
        file = open(file=path, mode='r')
    except:
        raise OSError("Error openning file.")

    return file


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
        # Doesn't account for string not containing a number
        digits = [char for char in line if char.isdigit()]
        values.append(int(digits[0]+digits[-1]))

    file.close()

    return sum(values)


### Part Two ###
# The problem now is that numbers can also be speled out, like "one", "two", "three", etc.
# I need to account for cases like 'eightwothree', where the first number is 'eight' and, because
# of that, there's no 'two'.

# First attempt: NOT WORKING
# Might be the worst solution i could come up with, in terms of complexity
def check_real_sum(file=''):
    '''
    Opens the file and for each line, creates a list of it's chracters. Then loops indefinitely:

        An auxiliar variable, `temp_num`, takes the value of the first character on the list. Then,
        checks if it's one of the nine valid numbers in the dict `{"one": "1", "two": "2", ..., "nine": "9"}`.
        If it is, replace the substring on the line with the equivalent number. If it's not, deletes the
        character from the list.

        After, makes the checks - if the list is not empty, the current character is appended to `temp_num`
        (this proccess composes a word that possibly matches a number on the dict) and the loop continues.
        If it is, checks if `temp_num` is empty, in which case, breaks out of the loop. Else, checks if the var
        has length > 2 (because the shortest word on the dict has lenth 3). If it does, the it's chars become the
        list and the loop repeats; else, break.

        Needles to say, terrible complexity...
    '''

    string_nums = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

    file = open_file(file)

    actual_lines = []
    for line in file:
        individual_chars = list(line)
        temp_num = ""
        while True:
            temp_char = individual_chars[0]
            temp_num += temp_char
            if ((temp_num in line) and (temp_num in string_nums.keys())):
                # if (temp_num in string_nums.keys()):
                    line = line.replace(temp_num, string_nums[temp_num])
                    temp_num = ""
            individual_chars = individual_chars[1::]
            if not(individual_chars):
                if not(temp_num): break
                if (len(temp_num) > 2):
                    individual_chars = list(temp_num[1::])
                    temp_num = ""
                else: break
        actual_lines.append(line[:-1])

    values = []
    for actual_line in actual_lines:
        digits = [char for char in actual_line if char.isdigit()]
        values.append(int(digits[0]+digits[-1]))

    file.close()

    return sum(values)

# Regex oh no: NOT IMPLEMENTED
import re
def check_real_sum2(file=''):
    string_nums = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

    file = open_file(file)

    for line in file:
        print(line)
        new_line = ""
        for k, v in string_nums.items():
            match_str = ""
            # Ideia (TODO):
            # Esse regex search retorna os index de início e de fim da pattern match.
            # Com esses números, dá pra comparar com os index de actual números na string pra ver quem aparece primeiro.
            # Além disso, dá pra usar isso aqui pra fazer pattern matching tbm:
                # for k, v in string_nums.items():
                #     if k in line:
                #         line.replace(k, v)
            if re.search(k, line):
                first_index = re.search(k, line).span()[0]
                last_index = re.search(k, line).span()[1]
                match_str = line[first_index:last_index]
                new_str = line.replace(match_str, v)
                print(new_str)

        print("")

# Second attempt: Valid
# I feel like i'm missing simething. There should be a better way to do this.
def second_alg(file=''):
    ''' Based on the idea:
        We divide the words in the dictionary into groups based on the length of each word.
        Then, we iterate through the line with a "block" of the size of each subgroup and we record each substring
        that belongs to the dictionary.
        We should also record the starting index of each substring to later retrieve the correct numbers.

        Example: abcone2threexyz
            Subgroups -> (size: [content]) = (3: [one, two, six]), (4: [four, five, nine]), (5: [three, seven, eight])

            Iterate with size 3; Is it in the subgroup?:
                [abc]one2threexyz = False\n
                a[bco]ne2threexyz = False\n
                ab[con]e2threexyz = False\n
                abc[one]2threexyz = True -> index=3\n
            And so on...
    '''

    file = open_file(file)

    string_nums = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

    actual_nums =[]
    for line in file:
        if (line[0].isdigit() and line[-2].isdigit()):
            first = int(line[0])
            last = int(line[-2])
            actual_nums.append(first*10+last)
            continue

        line = line[0:-1]
        indexes = {} # {index: "num"}
        step = 3
        while (step < 6):
            i = 0 # <- index
            while (step+i<len(line)+1):
                subline = line[0+i:step+i]
                if subline in string_nums.keys():
                    indexes[i]=string_nums[subline]
                i += 1
            step += 1

        digits = {index:char for index ,char in enumerate(line) if char.isdigit()}

        dall = {} # {index: "digit"}
        dall.update(indexes)
        dall.update(digits)

        # Sort indexes on dict:
        sorted_dict = dict(sorted(dall.items()))

        first = int(list(sorted_dict.values())[0])
        last = int(list(sorted_dict.values())[-1])

        actual_nums.append(first*10+last)

    return sum(actual_nums)


if __name__ == '__main__':
    main()
