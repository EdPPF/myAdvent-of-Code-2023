def main():
    print("Test = ", get_sum("Python/test.txt"))
    soma = get_sum("Python/schematic.txt")
    print("Input = ", soma)


def get_num(initial_index: int, line: str):
    the_number = ''

    temp_index = initial_index
    temp_num = line[initial_index]
    ## While there's a number on the left side, walk left until reaching a non-number or the beggining of the line
    while line[temp_index-1].isnumeric() and temp_index-1 >= 0:
        temp_index -= 1
        temp_num = line[temp_index]

    ## Now, walk right until reaching a non-number or end of line while composing the number
    while temp_num.isnumeric():
        the_number += temp_num
        temp_index += 1
        if temp_index <= len(line)-1:
            temp_num = line[temp_index]
        else:
            break

    return int(the_number)


def retrieve_num(line_index, target_line, target_list, temp_num):
    '''
    Gets number at `line_index` from `target_line` and appends to `target_list` only after
    performing a check - if the number retrieved from line is different from the immediate previous number.
    '''
    this_num = get_num(line_index, target_line)
    if this_num != temp_num:
        target_list.append(this_num)
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
                            temp_num = retrieve_num(prev_line_index, previous_line, sum_list, temp_num)

                        ## Left - same line; line below:
                        # if prev_line_index-1 >= 0: # If ther's a char on the left
                        #     ## Same line || Line below, left diagonal:
                        #     if previous_line[prev_line_index-1] in symbols or current_line[prev_line_index-1] in symbols:
                        #         temp_num = retrieve_num(prev_line_index, previous_line, sum_list, temp_num)

                        ## Same index - line below:
                        # if current_line[prev_line_index] in symbols:
                        #     temp_num = retrieve_num(prev_line_index, previous_line, sum_list, temp_num)

                        ## Rigth - same line; line below:
                        # if prev_line_index+1 < len(previous_line):
                        #     ## Same line || Line below, right diagonal:
                        #     if previous_line[prev_line_index+1] in symbols or current_line[prev_line_index+1] in symbols:
                        #         temp_num = retrieve_num(prev_line_index, previous_line, sum_list, temp_num)

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
                            temp_num = retrieve_num(next_line_index, next_line, sum_list, temp_num)

                        ## Left - same line || line below:
                        # if next_line_index-1 >= 0:
                        #     ## Same line || Line above, left diagonal:
                        #     if next_line[next_line_index-1] in symbols or current_line[next_line_index-1] in symbols:
                        #         temp_num = retrieve_num(next_line_index, next_line, sum_list, temp_num)

                        ## Same index - line above:
                        # if current_line[next_line_index] in symbols:
                        #     temp_num = retrieve_num(next_line_index, next_line, sum_list, temp_num)

                        ## Rigth - same line || line above:
                        # if next_line_index+1 < len(previous_line):
                        #     ## Same line || Line above, right diagonal:
                        #     if next_line[next_line_index+1] in symbols or current_line[next_line_index+1] in symbols:
                        #         temp_num = retrieve_num(next_line_index, next_line, sum_list, temp_num)

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
                        temp_num = retrieve_num(cur_line_index, current_line, sum_list, temp_num)

                    ## Left - line above; same line; line below:
                    # if cur_line_index-1 >= 0:
                    #     ## Line above, left diagonal || Same line || Line below, left diagonal:
                    #     if (
                    #         previous_line[cur_line_index-1] in symbols or
                    #         current_line[cur_line_index-1] in symbols or
                    #         next_line[cur_line_index-1] in symbols
                    #         ):
                    #         temp_num = retrieve_num(cur_line_index, current_line, sum_list, temp_num)

                    ## Same index - line above || line below:
                    # if previous_line[cur_line_index] in symbols or next_line[cur_line_index] in symbols:
                    #     temp_num = retrieve_num(cur_line_index, current_line, sum_list, temp_num)

                    ## Rigth - line above; same line; line below:
                    # if cur_line_index+1 < len(current_line):
                    #     ## Line above, rigth diagonal || Same line || Line below, right diagonal:
                    #     if (
                    #         previous_line[cur_line_index+1] in symbols or
                    #         current_line[cur_line_index+1] in symbols or
                    #         next_line[cur_line_index+1] in symbols
                    #         ):
                    #         temp_num = retrieve_num(cur_line_index, current_line, sum_list, temp_num)

    return sum(sum_list)


if __name__ == '__main__':
    main()
