fn main() {
    println!("{}", get_points("src/test.txt"));
    println!("{}", get_points("src/input.txt"));
}


use std::fs;
use regex::Regex as re;
fn file_parser(file: &str) -> String {
    let data: String = fs::read_to_string(file).expect("Unable to read file.");
    data
}

fn get_points(path: &str) -> i32 {
    let data: String = file_parser(path);
    let games: Vec<_> = data.lines().collect();

    let mut total_points: i32 = 0;
    for game in games {
        let mut game_points: i32       = 0;
        let separate       : Vec<&str> = game.split('|').collect();

        let match_expression: re = re::new(r"\d+").unwrap();
        let mut winning_numbers: Vec<&str> = match_expression
                                            .find_iter(separate[0])
                                            .map(|m| m.as_str())
                                            .collect();

        let game_id         : i32       = winning_numbers[0].parse().unwrap();
        winning_numbers                 = winning_numbers[1..winning_numbers.len()].to_vec();
        let obtained_numbers: Vec<&str> = match_expression
                                .find_iter(separate[1])
                                .map(|m| m.as_str())
                                .collect();

        for number in obtained_numbers {
            if winning_numbers.contains(&number) {
                game_points = if game_points == 0 {game_points+1} else {game_points*2};
            }
        }
        total_points += game_points;
    }

    total_points
}



////////// Unit Tests //////////
#[cfg(test)]
mod unit_tests {
    #[test]
    fn get_points_from_test() {
        assert_eq!(super::get_points("src/test.txt"), 13i32);
    }
    #[test]
    fn get_points_from_input() {
        assert_eq!(super::get_points("src/input.txt"), 26218i32);
    }
}
