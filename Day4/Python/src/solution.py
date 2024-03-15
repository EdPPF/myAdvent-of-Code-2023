def main():
    print(first_impact("test.txt"))
    print(first_impact("input.txt"))
    # print(second_impact("../input.txt"))
    # print(second_impact("../input.txt"))


class ScratchCard:
    def __init__(self, winning_nums: list[str], holding_nums: list[str], card_id: int) -> None:
        self.winning_numbers: list[str] = winning_nums
        self.holding_numbers: list[str] = holding_nums
        self.occurrences    : int  = 1
        self.id             : int  = card_id

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

    def points(self) -> int:
        """
        FOR PART 1 ONLY\n
        Returns the number of points this card is worth.
        """
        points = 0
        for num in self.holding_numbers:
            if num in self.winning_numbers:
                points = points+1 if points == 0 else points*2
        return points


def _open_file(path: str) -> list[str]:
    """
    Auxiliar function for opening input files.\n
    Returns:
        `list[str]`: A list of strings, each string being a line from the file.
    """
    with open(file=path) as arc:
        archive = arc.read().split('\n')
    return archive[:-1]


def _get_card_components(line: str) -> tuple[list[int], list[int], int]:
    """
    Auxiliar function\n
    Parses a line of input and extracts the card components.

    Args:
        `line (str)`: The input line containing the card components.

    Returns:
        `tuple[list[int], list[int], int]`: A tuple containing the win numbers, hold numbers, and card ID.
    """
    separated_nums: list[str] = line.split('|')

    win_nums = list(map(int, re.findall(r'\d+', separated_nums[0])))
    card_id: int = win_nums[0]
    win_nums: list[int] = win_nums[1:]
    hold_nums: list[int] = list(map(int, re.findall(r'\d+', separated_nums[1])))

    return win_nums, hold_nums, card_id

import re
#############################Part 1##############################
def first_impact(path:str) -> int:
    archive = _open_file(path)

    total = 0
    for line in archive:
        points = 0
        winning_numbers, obtained_numbers, card_id = _get_card_components(line)

        card = ScratchCard(winning_numbers, obtained_numbers, card_id)

        points = card.points()
        total += points

    return total

#############################Part 2##############################
def second_impact(path: str) -> int:
    archive = _open_file(path)

    cards_deck = {}
    scratches = []
    for line in archive:
        win_nums, hold_nums, card_id = _get_card_components(line)

        card = ScratchCard(win_nums, hold_nums, card_id)
        cards_deck[card] = card.get_matches()
        scratches.append(card)

    keys = list(cards_deck.keys())
    for i in range(len(keys)):
        current_card = keys[i]
        current_times = cards_deck[current_card]
        if current_times == 0:
            continue

        for j in range(current_card.id, current_card.id + current_times):
            next_card = keys[j]
            next_card.add_occurrence(current_card.occurrences)

    total = 0
    for card in cards_deck:
        total += card.occurrences

    return total


if __name__ == "__main__":
    main()
