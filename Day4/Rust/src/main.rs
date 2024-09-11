fn main() {
    // println!("{}", get_points("src/test.txt"));
    // println!("{}", get_points("src/input.txt"));
    second_impact("src/test.txt");
}


use std::{collections::HashMap, fs};
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


//###########################Part 2##############################
#[derive(Eq, Hash, PartialEq, Clone)]
struct ScratchCard {
    winning_numbers: Vec<i32>,
    holding_numbers: Vec<i32>,
    occurrences    : i32,
    id             : i32,
}

impl ScratchCard {
    fn new(id: i32, winning_numbers: Vec<i32>, holding_numbers: Vec<i32>) -> ScratchCard {
        ScratchCard {
            id,
            winning_numbers,
            holding_numbers,
            occurrences : 0,
        }
    }

    fn add_occurrence(&mut self, times: &i32) {
        self.occurrences += times;
    }

    fn get_matches(&self) -> i32{
        let mut counter: i32 = 0;
        for num in self.holding_numbers.iter() {
            if self.holding_numbers.contains(num) {
                counter += 1;
            }
        }
        counter
    }
}


fn second_impact(path: &str) -> i32 {
    let data: String = file_parser(path);
    let cards: Vec<_> = data.lines().collect();

    let mut card_set: HashMap<ScratchCard, i32> = HashMap::new();
    for card in cards {
        let separated_nums: Vec<&str> = card.split('|').collect();

        let match_expression: re = re::new(r"\d+").unwrap();
        let mut winning_numbers: Vec<&str> = match_expression
                            .find_iter(separated_nums[0])
                            .map(|m| m.as_str())
                            .collect();

        let card_id: i32 = winning_numbers[0].parse().unwrap();
        winning_numbers = winning_numbers[1..].to_vec();
        let holding_numbers: Vec<&str> = match_expression
                        .find_iter(separated_nums[1])
                        .map(|m| m.as_str())
                        .collect();

        let winning_numbers: Vec<i32> = winning_numbers.iter().map(|&x| x.parse().unwrap()).collect();
        let holding_numbers: Vec<i32> = holding_numbers.iter().map(|&x| x.parse().unwrap()).collect();

        let card: ScratchCard = ScratchCard::new(card_id, winning_numbers, holding_numbers);
        card_set.insert(card, card_id);

        let keys: Vec<ScratchCard> = card_set.keys().cloned().collect();
        for i in 0..keys.len() {
            let current_card: &ScratchCard = &keys[i];
            let current_times: &i32 = card_set.get(current_card).unwrap();
            if current_times == &0i32 {
                continue;
            }
            for _ in 0..current_card.occurrences {
                for j in current_card.id..(current_card.id + current_times) {
                    let mut next_card: &ScratchCard = &keys[j as usize];
                    next_card.add_occurrence();
                }
            }
        }
    }
    let mut total_points: i32 = 0;
    for card in card_set.keys() {
        total_points += card.occurrences;
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
