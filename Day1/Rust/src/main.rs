fn main() {
    // let solution: u32 = get_sum("src/values.txt");
    // println!("Solution for 'src/values.txt': {}", solution);

    // let solution: u32 = get_sum("src/test.txt");
    // println!("Solution for 'src/test.txt': {}", solution);

    println!("{:?}", get_real_sum("src/values.txt"));
}

use std::{fs, collections::HashMap};

fn file_parser(file: &str) -> String {
    let data: String = fs::read_to_string(file).expect("Unable to read file");
    data
}

/// First attempt: Valid
/// This feels convoluted and i'm not sure if it's following good practices, but it works.
#[allow(unused)]
fn get_sum(file: &str) -> u32 {
    let data: String = file_parser(file);

    let mut result: u32 = 0;
    for line in data.lines() {
        // This returns the index of the first numeric char
        let first_num_index: usize = line.find(char::is_numeric).unwrap();
        // This gets the char at the index, already as integer
        let first_num: u32= line.chars().nth(first_num_index).unwrap().to_digit(10).unwrap();
        // println!("[{}] = {}", first_num_index, first_num);

        // Same as above, but for the last numeric char
        let last_num_index: usize = line.rfind(char::is_numeric).unwrap();
        let last_num: u32 = line.chars().nth(last_num_index).unwrap().to_digit(10).unwrap();
        // println!("[{}] = {}", last_num_index, last_num);

        // println!("----{}----", first_num * 10 + last_num); // Matematica

        result += first_num * 10 + last_num;
    }
    result
}

// Solution Idea:
// While parsing through the file, on each line, start from the beginning
// and the end of the string until finding a number. Take those numbers
// to form the two digit value.
    // What can be used:
        // The retain method: https://doc.rust-lang.org/std/string/struct.String.html#method.retain
        // It takes a String and MODIFIES IT such that it retains only the specified chars. As in the
        // example, we can use it to delete the occurences of the specified character, which could be
        // used to retain only numeric chars.


////////// Part Two //////////
// The problem now is that numbers can also be speled out, like "one", "two", "three", etc.
// I need to account for cases like 'eightwothree', where the first number is 'eight' and, because
// of that, there's no 'two'.

// https://stackoverflow.com/questions/53688202/does-rust-have-an-equivalent-to-pythons-dictionary-comprehension-syntax
// Thos link has the following answer:
    // Rust's iterators have map/filter/collect methods which are enough to do anything Python's comprehensions can.
    // You can create a HashMap with collect on an iterator of pairs, but collect can return various types of
    // collections, so you may have to specify the type you want.
// I think that's enough to translate my Python solution.

/// First attempt: Valid
/// Pretty much a translation of my Python solution. Rust's syntax required some changes, but the idea is the same.
fn get_real_sum(file: &str) -> u32 {
    let data: String = file_parser(file);

    let numbers_dict: HashMap<&str, &str> = HashMap::from([
        ("one",   "1"),
        ("two",   "2"),
        ("three", "3"),
        ("four",  "4"),
        ("five",  "5"),
        ("six",   "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine",  "9"),
    ]);

    let mut actual_nums: Vec<u32> = vec![]; // List of results
    for line in data.lines() {
        let mut indexes: HashMap<u32, String> = HashMap::new(); // {index: "num"}

        // First char of line:
        let line_zero_byte: u8 = line.as_bytes()[0];
        let line_zero: char = line_zero_byte as char;
        // Last char of line:
        let line_last_byte: u8 = line.as_bytes()[line.len()-1];
        let line_last: char = line_last_byte as char;

        if line_zero.is_numeric() && line_last.is_numeric() {
            let first: u32 = line_zero.to_digit(10).unwrap();
            let last:  u32 = line_last.to_digit(10).unwrap();
            actual_nums.push(
                first*10 + last
            );
            continue;
        }

        // Collects the spelled numbers and their starting indexes:
        let mut step: u8 = 3;
        while step < (line.len()+1).try_into().unwrap() && step < 6 {
            let mut offset: u32 = 0;
            for window in line.chars().collect::<Vec<char>>().windows(step.into()) {
                let slice: String = window.iter().collect();
                if numbers_dict.contains_key(slice.as_str()) {
                    indexes.insert(offset.into(), numbers_dict.get(slice.as_str()).unwrap().to_string());
                }
                offset += 1;
            }
            step += 1;
        }

        // Collects the numbers (not spelled) on the line:
        let mut numbers_indexes: HashMap<u32, String> = HashMap::new();
        for (index, num) in line.chars().enumerate().filter(|(_, c)| c.is_numeric()) {
            numbers_indexes.insert(index.try_into().unwrap(), String::from(num)); // -> index: "num"
        }

        // "Merge" two dicts:
        indexes.extend(numbers_indexes);

        let mut bigger = indexes.iter().next().unwrap().0;
        let mut smaller = indexes.iter().next().unwrap().0;
        for (index, _) in indexes.iter() {
            if smaller > index {
                smaller = index;
            }
            if bigger < index {
                bigger = index;
            }
        }

        let unit = indexes.get(&smaller).unwrap().parse::<u32>().unwrap();
        let dec = indexes.get(&bigger).unwrap().parse::<u32>().unwrap();
        actual_nums.push(unit*10 + dec);
    };

    return {
        let mut result: u32 = 0;
        for num in actual_nums {
            result += num;
        }
        result
    }
}


// Not really necessary, but still
#[cfg(test)]
mod unit_tests {
    #[test]
    fn get_sum_from_test() {
        assert_eq!(super::get_sum("src/test.txt"), 142);
    }

    #[test]
    fn get_sum_from_values() {
        assert_eq!(super::get_sum("src/values.txt"), 55123);
    }

    #[test]
    fn get_real_sum_from_test2() {
        assert_eq!(super::get_real_sum("src/test2.txt"), 281);
    }

    #[test]
    fn get_real_sum_from_values() {
        assert_eq!(super::get_real_sum("src/values.txt"), 55260);
    }
}
