# This problem seems as simple as to parse the strings of the file and check if the amount of
# cubes make sense within the game's configuration.

# Since i'm using different folders for each day, i'll just re-write functions i can reuse...


def main():
    print(get_valid_games_sum('test.txt'))
    print(get_valid_games_sum('values.txt'))


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
            # Gets cubes pulles for each set:
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



if __name__ == '__main__':
    main()
