def main():
    print(get_points("test.txt"))
    print(get_points("input.txt"))


## I'm resorting to regex... For no particular reason though.
import re
def get_points(path:str) -> int:
    with open(file=path) as arc:
        archive = arc.read().split('\n')

    total: int = 0
    for line in archive[:-1]:
        points  : int       = 0
        separate: list[str] = line.split('|')

        winning_numbers = list(map(int, re.findall(r'\d+', separate[0])))
        game_id         : int       = winning_numbers[0]
        winning_numbers : list[int] = winning_numbers[1:]
        obtained_numbers: list[int] = list(map(int, re.findall(r'\d+', separate[1])))

        for number in obtained_numbers:
            if number in winning_numbers:
                points = points+1 if points == 0 else points*2
                # if points == 0:
                #     points += 1
                # else:
                #     points *= 2
        total += points

    return total


if __name__ == "__main__":
    main()
