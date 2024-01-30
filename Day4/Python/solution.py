def main():
    # print(get_points("test.txt", False))
    # print(get_points("input.txt", False))
    # print(second_impact("test.txt"))
    print(second_impact("input.txt"))


## I'm resorting to regex... For no particular reason though.
import re
def get_points(path:str, part_two: bool) -> int | dict[int, list[int]]:
    with open(file=path) as arc:
        archive = arc.read().split('\n')

    total         : int                  = 0
    returning_dict: dict[int, list[int]] = {}
    for line in archive[:-1]:
        points           : int       = 0
        separate         : list[str] = line.split('|')
        returning_numbers: list[int] = []

        winning_numbers = list(map(int, re.findall(r'\d+', separate[0])))
        game_id         : int       = winning_numbers[0]
        winning_numbers : list[int] = winning_numbers[1:]
        obtained_numbers: list[int] = list(map(int, re.findall(r'\d+', separate[1])))

        for number in obtained_numbers:
            if number in winning_numbers:
                returning_numbers.append(number)
                points = points+1 if points == 0 else points*2
        returning_dict[game_id] = returning_numbers
        total += points

    return returning_dict if part_two else total


#############################Part 2##############################
def get_sub_dicts(og_dict: dict[int, list[int]], cur_key: int) -> dict[int, list[int]]:
    returning_dict: dict[int, list[int]] = {}
    size: int = len(og_dict[cur_key])
    for i in range(cur_key+1, cur_key+size+1):
        if i > len(og_dict):
            break
        returning_dict[i] = og_dict[i]
    return returning_dict

def compose_sub_dicts(cur_dict: dict[int, list[int]], og_dict: dict[int, list[int]]) -> dict[int, list[int]]:
    for key in cur_dict.keys():
        sub_dict = get_sub_dicts(og_dict, key)
        yield sub_dict

import pprint
pp = pprint.PrettyPrinter(indent=4)
def second_impact(path:str) -> int:
    cards_dict : dict[int, list[int]]       = get_points(path, True)
    og_list    : list[dict[int, list[int]]] = [cards_dict]
    master_list: list[dict[int, list[int]]] = []

    cur_list = og_list
    while cur_list != [{}]:
        temp_list = []
        for dictio in cur_list:
            gen = compose_sub_dicts(dictio, cards_dict)
            sub_list = []
            while True:
                try:
                    sub_list.append(next(gen))
                except StopIteration:
                    break
            master_list += sub_list
            temp_list += sub_list
        cur_list = temp_list
        pp.pprint(cur_list)
        break

    # sum_points = 0
    # for dictio in master_list:
    #     sum_points += len(dictio)
    # for ogicts in og_list:
    #     sum_points += len(ogicts)
    sum_points = sum(len(dictio) for dictio in master_list + og_list)
    return sum_points


if __name__ == "__main__":
    main()
