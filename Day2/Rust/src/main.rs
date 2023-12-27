fn main() {
    println!("Test: {}", get_valid_games_sum("src/test.txt"));
    println!("Values: {}", get_valid_games_sum("src/values.txt"));
}


use std::fs;
fn file_parser(file: &str) -> String {
    let data: String = fs::read_to_string(file).expect("Unable to read file.");
    data
}

// First attempt - Python solution translation:
fn get_valid_games_sum(file: &str) -> u32 {
    let data: String = file_parser(file);

    let red_quantity  : u32 = 12;
    let green_quantity: u32 = 13;
    let blue_quantity : u32 = 14;

    let mut possible_games: Vec<u32> = vec![];
    for line in data.lines() {
        let mut game_possible: bool = true;
        // Gets game ID:
        let game_id: u32 = {
                if line[6..7].parse::<char>().unwrap() == ':' {
                // parse() is used to convert the string into another type.
                // unwrap() is to get the new value the string was converted into.
                line[5..6].parse().unwrap()
            }
            else if line[7..8].parse::<char>().unwrap() == ':' {
                // nth() returns Option<Self::Item>, so we need to get the value with unwrap()
                // line.chars().nth(5).unwrap() as u32 // -> Not working, for some reason
                line[5..7].parse().unwrap()
            }
            else {
                line[5..8].parse().unwrap()
            }
        };

        // Gets sets of cubes for this game:
        let game_sets: Vec<&str> = { // -> ['5 green, 6 blue, 1 red']
            if line[7..8].parse::<char>().unwrap() == ' ' {
                line[8..].split("; ").collect()
            }
            // This accounts for the 100th line, where the ' ' is in the 9th position
            else if line[9..10].parse::<char>().unwrap() == ' ' {
                line[10..].split("; ").collect()
            }
            else {
                line[9..].split("; ").collect()
            }
        };

        'current_game: for set in game_sets {
            // Gets cubes pulls for each set:
            let pulls: Vec<&str> = set.split(", ").collect(); // -> ["5 green", "6 blue", "1 red"]

            for cubes in pulls {
                // Gets quantity on this pull:
                let cube_quantity: u32 = {
                    if cubes[1..2].parse::<char>().unwrap() == ' ' {
                        cubes[0..1].parse().unwrap() // -> 5
                    }
                    else {
                        cubes[0..2].parse().unwrap()
                    }
                };
                // Gets cube type (color) on this pull:
                let cube_type: &str = {
                    if cubes[1..2].parse::<char>().unwrap() == ' ' {
                        &cubes[2..] // -> "green"
                    }
                    else {
                        &cubes[3..]
                    }
                };

                // Check if the cube quantity is NOT within boundaries of it's type according to game rules,
                // in which case, stop analysing the current set:
                match cube_type {
                    "red" => if cube_quantity > red_quantity {
                        game_possible = false;
                        continue 'current_game;
                    },
                    "green" => if cube_quantity > green_quantity {
                        game_possible = false;
                        continue 'current_game;
                    },
                    "blue" => if cube_quantity > blue_quantity {
                        game_possible = false;
                        continue 'current_game;
                    },
                    &_ => println!("Invalid Color.") // This should never happen
                }
            }
        }
        if game_possible {
            possible_games.push(game_id);
        }
    }

    possible_games.iter().sum()
}


#[cfg(test)]
mod unit_tests {
    #[test]
    fn get_valid_games_sum_from_test() {
        assert_eq!(super::get_valid_games_sum("src/test.txt"), 8);
    }

    #[test]
    fn get_valid_games_sum_from_values() {
        assert_eq!(super::get_valid_games_sum("src/values.txt"), 2149);
    }
}
