def main():
    print("Test = ", get_sum("test.txt"))
    print("Input = ", get_sum("schematic.txt"))

    print(get_gears("test.txt"))
    print(get_gears("schematic.txt"))


def get_num(initial_index: int, line: str):
    the_number   = ''
    indexes_list = []

    temp_index = initial_index
    temp_num = line[initial_index]
    ## While there's a number on the left side, walk left until reaching a non-number or the beggining of the line
    while line[temp_index-1].isnumeric() and temp_index-1 >= 0:
        temp_index -= 1
        temp_num = line[temp_index]

    ## Now, walk right until reaching a non-number or end of line while composing the number
    while temp_num.isnumeric():
        indexes_list.append(temp_index)
        the_number += temp_num
        temp_index += 1
        if temp_index <= len(line)-1:
            temp_num = line[temp_index]
        else:
            break

    return (int(the_number), indexes_list)


def retrieve_num(
        line_index         : int,
        target_line        : str,
        target_numbers_list: list,
        target_indexes_list: list,
        temp_num           : int,
        line_position      : int
    ):
    '''
    Gets number at `line_index` from `target_line` and appends to `target_numbers_list` only after
    performing a check - if the number retrieved from line is different from the immediate previous number.

    Outside all that, it is checked if the indexes of the number retrieved were already accounted before on the
    external list `target_indexes_list`, taking into account which line they are located.
    '''
    this_num, indexes = get_num(line_index, target_line)
    if (indexes, line_position) not in target_indexes_list:
        target_indexes_list.append((indexes, line_position))
        if this_num != temp_num:
            target_numbers_list.append(this_num)
            temp_num = this_num
        return temp_num


def get_sum(arch: str):
    symbols = "*@#$+-=%/&"

    with open(arch) as file:
        lines = file.read().split('\n')
    lines = lines[:-1]

    sum_list = []

    for index, line in enumerate(lines):
        temp_num = 0

        if (((index+1) < len(lines)) and ((index - 1) >= 0)):
            previous_line = lines[index-1]
            current_line  = line
            next_line     = lines[index+1]

            ## If previous_line is the first line of the input:
            if index-1 == 0:
                ## Check if numbers on previous_line are adj to symbols on current_line:
                for prev_line_index, num in enumerate(previous_line):
                    if num.isnumeric():
                        ## I'm not sure if this is better or worse than sepparating the `ìf`s.
                        ## Leaving the second option as comments just so i remember
                        if (
                            ## Left - same line; line below:
                            prev_line_index-1 >= 0 and
                            (
                                ## Same line || Line below, left diagonal:
                                previous_line[prev_line_index-1] in symbols or
                                current_line[prev_line_index-1] in symbols
                            )
                        ) or (
                            ## Same index - line below:
                            current_line[prev_line_index] in symbols
                        ) or (
                            ## Rigth - same line; line below:
                            prev_line_index+1 < len(previous_line) and
                            (
                                ## Same line || Line below, right diagonal:
                                previous_line[prev_line_index+1] in symbols or
                                current_line[prev_line_index+1] in symbols
                            )
                        ):
                            temp_num = retrieve_num(prev_line_index, previous_line, sum_list, [], temp_num, index)

            ## If next line is the last line of the input:
            if index+2 == len(lines): # Using 'index+2' because we reach maximum index of 138
                ## Check if numbers on next_line are adj to symbols on current_line:
                for next_line_index, num in enumerate(next_line):
                    if num.isnumeric():
                        if (
                            ## Left - same line || line below:
                            next_line_index-1 >= 0 and
                            (
                                ## Same line || Line above, left diagonal:
                                next_line[next_line_index-1] in symbols or
                                current_line[next_line_index-1] in symbols
                            )
                        ) or (
                            ## Same index - line above:
                            current_line[next_line_index] in symbols
                        ) or (
                            ## Rigth - same line || line above:
                            next_line_index+1 < len(previous_line) and
                            (
                                ## Same line || Line above, right diagonal:
                                next_line[next_line_index+1] in symbols or
                                current_line[next_line_index+1] in symbols
                            )
                        ):
                            temp_num = retrieve_num(next_line_index, next_line, sum_list, [], temp_num, index)

            ## Check if numbers on current_line are adj to symbols on previous_line or next_line:
            for cur_line_index, num in enumerate(current_line):
                if num.isnumeric():
                    if (
                        ## Left - line above; same line; line below:
                        cur_line_index-1 >= 0 and
                        (
                            ## Line above, left diagonal || Same line || Line below, left diagonal:
                            previous_line[cur_line_index-1] in symbols or
                            current_line[cur_line_index-1] in symbols or
                            next_line[cur_line_index-1] in symbols
                        )
                    ) or (
                        ## Same index - line above || line below:
                        previous_line[cur_line_index] in symbols or
                        next_line[cur_line_index] in symbols
                    ) or (
                        ## Rigth - line above; same line; line below:
                        cur_line_index+1 < len(current_line) and
                        (
                            ## Line above, rigth diagonal || Same line || Line below, right diagonal:
                            previous_line[cur_line_index+1] in symbols or
                            current_line[cur_line_index+1] in symbols or
                            next_line[cur_line_index+1] in symbols
                        )
                    ):
                        temp_num = retrieve_num(cur_line_index, current_line, sum_list, [], temp_num, index)

    return sum(sum_list)


#############################Part 2##############################
## This part asks two find '*' adjacent to exactly two numbers.
## The algorithm follows the same idea as the first one.

def get_gears(arch: str):
    with open(arch) as file:
        lines = file.read().split('\n')
    lines = lines[:-1]

    master_list = []

    for index, line in enumerate(lines):
        temp_num = 0

        if (((index+1) < len(lines)) and ((index - 1) >= 0)):
            previous_line = lines[index-1]
            current_line  = line
            next_line     = lines[index+1]

            ## If previous_line is the first line of the input:
            if index-1 == 0:
                if '*' in previous_line:
                    ## Check if * on previous_line are adj to 2 numbers on current_line:
                    for prev_line_index, gear in enumerate(previous_line):
                        first_line_nums    = []
                        first_line_indexes = []
                        if gear == '*':
                            ## Left - same line; line below:
                            if prev_line_index-1 >= 0: # If ther's a char on the left
                                ## Same line:
                                if previous_line[prev_line_index-1].isnumeric():
                                    temp_num = retrieve_num(prev_line_index-1, previous_line, first_line_nums, first_line_indexes, temp_num, index)
                                ## Line below, left diagonal:
                                if current_line[prev_line_index-1].isnumeric():
                                    temp_num = retrieve_num(prev_line_index-1, current_line, first_line_nums, first_line_indexes, temp_num, index+1)

                            ## Same index - line below:
                            if current_line[prev_line_index].isnumeric():
                                temp_num = retrieve_num(prev_line_index, current_line, first_line_nums, first_line_indexes, temp_num, index+1)

                            ## Rigth - same line; line below:
                            if prev_line_index+1 < len(previous_line):
                                ## Same line:
                                if previous_line[prev_line_index+1].isnumeric():
                                    temp_num = retrieve_num(prev_line_index+1, previous_line, first_line_nums, first_line_indexes, temp_num, index)
                                ## Line below, right diagonal
                                if current_line[prev_line_index+1].isnumeric():
                                    temp_num = retrieve_num(prev_line_index+1, current_line, first_line_nums, first_line_indexes, temp_num, index+1)

                        ## If there's exactly 2 numbers adjacent to '*':
                        if len(first_line_nums) == 2:
                            master_list.append(first_line_nums[0]*first_line_nums[1])

            ## If next line is the last line of the input:
            if index+2 == len(lines): # Using 'index+2' because we reach maximum index of 138
                if '*' in next_line:
                    ## Check if numbers on next_line are adj to symbols on current_line:
                    for next_line_index, gear in enumerate(next_line):
                        last_line_nums    = []
                        last_line_indexes = []
                        if gear == '*':
                            ## Left - same line || line above:
                            if next_line_index-1 >= 0:
                                ## Same line:
                                if next_line[next_line_index-1].isnumeric():
                                    temp_num = retrieve_num(next_line_index-1, next_line, last_line_nums, last_line_indexes, temp_num, index)
                                ## Line above, left diagonal
                                if current_line[next_line_index-1].isnumeric():
                                    temp_num = retrieve_num(next_line_index-1, current_line, last_line_nums, last_line_indexes, temp_num, index-1)

                            ## Same index - line above:
                            if current_line[next_line_index].isnumeric():
                                temp_num = retrieve_num(next_line_index, current_line, last_line_nums, last_line_indexes, temp_num, index-1)

                            ## Rigth - same line || line above:
                            if next_line_index+1 < len(previous_line):
                                ## Same line:
                                if next_line[next_line_index+1].isnumeric():
                                    temp_num = retrieve_num(next_line_index+1, next_line, last_line_nums, last_line_indexes, temp_num, index)
                                ## Line above, right diagonal:
                                if current_line[next_line_index+1].isnumeric():
                                    temp_num = retrieve_num(next_line_index+1, current_line, last_line_nums, last_line_indexes, temp_num, index-1)

                        ## If there's exactly 2 numbers adjacent to '*':
                        if len(last_line_nums) == 2:
                            master_list.append(last_line_nums[0]*last_line_nums[1])

            if '*' in current_line:
                ## Check if numbers on current_line are adj to symbols on previous_line or next_line:
                for cur_line_index, gear in enumerate(current_line):
                    cur_line_nums    = []
                    cur_line_indexes = []
                    if gear == '*':
                        ## Left - line above; same line; line below:
                        if cur_line_index-1 >= 0:
                            ## Line above, left diagonal:
                            if previous_line[cur_line_index-1].isnumeric():
                                temp_num = retrieve_num(cur_line_index-1, previous_line, cur_line_nums, cur_line_indexes, temp_num, index-1)
                            ## Same line
                            if current_line[cur_line_index-1].isnumeric():
                                temp_num = retrieve_num(cur_line_index-1, current_line, cur_line_nums, cur_line_indexes, temp_num, index)
                            ## Line below, left diagonal:
                            if next_line[cur_line_index-1].isnumeric():
                                temp_num = retrieve_num(cur_line_index-1, next_line, cur_line_nums, cur_line_indexes, temp_num, index+1)

                        ## Same index - line above:
                        if previous_line[cur_line_index].isnumeric():
                            temp_num = retrieve_num(cur_line_index, previous_line, cur_line_nums, cur_line_indexes, temp_num, index-1)
                        ## Same index - line below:
                        if next_line[cur_line_index].isnumeric():
                            temp_num = retrieve_num(cur_line_index, next_line, cur_line_nums, cur_line_indexes, temp_num, index+1)

                        ## Rigth - line above; same line; line below:
                        if cur_line_index+1 < len(current_line):
                            ## Line above, rigth diagonal:
                            if previous_line[cur_line_index+1].isnumeric():
                                temp_num = retrieve_num(cur_line_index+1, previous_line, cur_line_nums, cur_line_indexes, temp_num, index-1)
                            ## Same line:
                            if current_line[cur_line_index+1].isnumeric():
                                temp_num = retrieve_num(cur_line_index+1, current_line, cur_line_nums, cur_line_indexes, temp_num, index)
                            ## Line below, right diagonal:
                            if next_line[cur_line_index+1].isnumeric():
                                temp_num = retrieve_num(cur_line_index+1, next_line, cur_line_nums, cur_line_indexes, temp_num, index+1)

                    ## If there's exactly 2 numbers adjacent to '*':
                    if len(cur_line_nums) == 2:
                        master_list.append(cur_line_nums[0]*cur_line_nums[1])

    return sum(master_list)

if __name__ == '__main__':
    main()
