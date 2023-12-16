fn main() {
    let solution: u32 = get_sum("src/values.txt");
    println!("Solution for 'src/values.txt': {}", solution);

    let solution: u32 = get_sum("src/test.txt");
    println!("Solution for 'src/test.txt': {}", solution);
}

use std::fs;

/// First attempt: Valid
/// This feels convoluted and i'm not sure if it's following good practices, but it works.
fn get_sum(file: &str) -> u32 {
    let data: String = fs::read_to_string(file).expect("Unable to read file");

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
