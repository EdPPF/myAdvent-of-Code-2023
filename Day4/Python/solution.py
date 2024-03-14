def main():
    # print(get_points("test.txt", False))
    # print(get_points("input.txt", False))
    print(second_impact("./input.txt"))
    # print(second_impact("Python/input.txt"))


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
class ScratchCard:
    def __init__(self, winning_nums: list[str], holding_nums: list[str], card_id: int) -> None:
        self.winning_numbers: list[str] = winning_nums
        self.holding_numbers: list[str] = holding_nums
        self.occurrences    : int  = 1
        self.id        : int  = card_id

    def add_occurrence(self, times) -> None:
        self.occurrences += times

    def get_matches(self) -> int:
        """
        Returns the number of itens that appear both on `self.winning_numbers` and
        `self.holding_numbers`.
        """
        counter = 0
        for num in self.holding_numbers:
            if num in self.winning_numbers:
                counter += 1
        return counter


def second_impact(path: str) -> int:
    with open(file=path) as arc:
        archive = arc.read().split('\n')
    archive = archive[:-1]

    adict = {}
    scratches = []
    for card in archive:
        separated_nums = card.split('|')

        win_nums = re.findall(r'\d+', separated_nums[0])
        card_id = int(win_nums[0])
        win_nums = win_nums[1:]
        hold_nums = re.findall(r'\d+', separated_nums[1])

        card = ScratchCard(win_nums, hold_nums, card_id)
        adict[card] = card.get_matches()
        scratches.append(card)

    keys = list(adict.keys())
    for i in range(len(keys)):
        current_card = keys[i]
        current_times = adict[current_card]
        if current_times == 0:
            continue

        for j in range(current_card.id, current_card.id + current_times):
            next_card = keys[j]
            next_card.add_occurrence(current_card.occurrences)

    total = 0
    for card in adict:
        total += card.occurrences

    return total


if __name__ == "__main__":
    main()
