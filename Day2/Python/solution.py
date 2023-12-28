# This problem seems as simple as to parse the strings of the file and check if the amount of
# cubes make sense within the game's configuration.

# Since i'm using different folders for each day, i'll just re-write functions i can reuse...


def main():
    # print(get_valid_games_sum('test.txt'))
    # print(get_valid_games_sum('values.txt'))
    print(get_games_power_sum('test.txt'))
    print(get_games_power_sum('values.txt'))


# Auxiliar function for opening files.
def open_file(path=""):
    try:
        file = open(file=path, mode='r')
    except:
        raise OSError("Error openning file.")

    return file

# First attempt: Valid
# This solution was made pretty smoothly. It looks well structured for me,
# but i'll still think if i can improve it. Two things that comes to mind are that swicth-case
# and how can i break out of the outermost loop without those `if possible_game == False` (this is easier in Rust...)
def get_valid_games_sum(file=''):
    file = open_file(file)

    red_quantity   = 12
    green_quantity = 13
    blue_quantity  = 14

    possible_games = []
    for line in file:
        possible_game: bool = True
        # Gets game ID:
        game_ID = int(line[5] if line[6] == ':' else line[5:7] if line[7] == ':' else line[5:8])
        # Gets sets of cubes for this game:
        game_sets = line[8:-1].split('; ') if line[7] == ' ' else line[9:-1].split('; ') # -> ['5 green, 6 blue, 1 red']

        for set in game_sets:
            # Gets cubes pulls for each set:
            pulls = set.split(', ') # -> ['5 green', '60 blue', '1 red']

            for cubes in pulls:
                # Gets quantity AND the cube type on this pull:
                if cubes[1] == ' ':
                    cube_quantity = cubes[0] # -> '5'
                    cube_type = cubes[2:] # -> 'green'
                else:
                    cube_quantity = cubes[0:2]
                    cube_type = cubes[3:]

                # Check if the cube quantity is NOT within boundaries of it's type according to game rules:
                match cube_type:
                    case 'red':
                        if int(cube_quantity) > red_quantity:
                            possible_game = False
                        # break
                    case 'green':
                        if int(cube_quantity) > green_quantity:
                            possible_game = False
                        # break
                    case 'blue':
                        if int(cube_quantity) > blue_quantity:
                            possible_game = False
                        # break

                if possible_game == False:
                    break
            if possible_game == False:
                    break

        if possible_game == True:
            possible_games.append(game_ID)

    return sum(possible_games)

#############################Part 2##############################
# The problem now is: On each game, what is the minimun amount of each cube that makes THE GAME possible?
# To solve this problem, i could evaluate the whole game (all sets of cubes) and get THE MAXIMUM values
# of each type of cube.
# The answer to the problem is the sum of each game's Power, which is the product of each value.

# For this, since i'm planning on reusing the same idea of the first part, i might refactor some code into
# their own function. Eventually

# First attempt: Valid
def get_games_power_sum(file:str) -> int:
    file = open_file(file)

    power_list: list[int] = []
    for game in file:
        game_dict: dict = {'red': 0, 'blue': 0, 'green': 0}
        game_power: int = 1

        # Gets sets of cubes for this game:
        game_sets = game[8:-1].split('; ') if game[7] == ' ' else game[9:-1].split('; ') # -> ['5 green, 6 blue, 1 red']

        for set in game_sets:
            # Gets cubes pulls for each set:
            pulls = set.split(', ') # -> ['5 green', '60 blue', '1 red']

            for cubes in pulls:
                # Gets quantity AND the cube type on this pull:
                if cubes[1] == ' ':
                    cube_quantity = int(cubes[0]) # -> '5'
                    cube_type = cubes[2:] # -> 'green'
                else:
                    cube_quantity = int(cubes[0:2])
                    cube_type = cubes[3:]

                # update game_dict with highest value of each color:
                if cube_quantity > game_dict[cube_type]:
                    game_dict[cube_type] = cube_quantity

        for (_, value) in game_dict.items():
            game_power *= value
        power_list.append(game_power)

    return sum(power_list)


if __name__ == '__main__':
    main()
