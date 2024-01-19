fn main() {
    println!("Test: {}", get_sum("src/test.txt"));
    println!("Input: {}", get_sum("src/schematic.txt"));

    println!("Test: {}", get_gears("src/test.txt"));
    println!("Input: {}", get_gears("src/schematic.txt"));
}


use std::{fs, vec};
fn file_parser(file: &str) -> String {
    let data: String = fs::read_to_string(file).expect("Unable to read file.");
    data
}


/// Getting number at specified index: Working
fn get_number(initial_index: usize, line: &str) -> (i32, Vec<i32>) {
    let mut the_number  : String   = String::from("");
    let mut indexes_list: Vec<i32> = vec![];

    let mut temp_index: i32    = initial_index as i32;
    let mut temp_size: usize   = initial_index;
    let mut temp_num: char     = line.chars().nth(temp_size).unwrap();

    // While there's a number on the left side, walk left until reaching a non-number or the beggining of the line
    while (temp_index - 1) >= 0 {
        if !line.chars().nth(temp_size-1).unwrap().is_numeric() {
            break;
        }
        temp_index -= 1;
        temp_size = temp_index as usize;
        temp_num = line.chars().nth(temp_size).unwrap();
    }

    // Now, walk right until reaching a non-number or end of line while composing the number
    while temp_num.is_numeric() {
        indexes_list.push(temp_index);
        the_number += &temp_num.to_string();
        temp_index += 1;
        temp_size = temp_index as usize;
        if temp_size <= line.len()-1 {
            temp_num = line.chars().nth(temp_size).unwrap();
        }
        else {
            break;
        }
    }
    (the_number.parse::<i32>().unwrap(), indexes_list)
}


fn retrieve_number(
    line_index         : usize,
    target_line        : &str,
    target_numbers_list: &mut Vec<i32>,
    target_indexes_list: &mut Vec<(Vec<i32>, i32)>, // -> [([45, 46, 47], 23)]
    mut temp_num       : i32,
    line_position      : i32
) -> i32 {
    let (this_num, indexes) = get_number(line_index, target_line);
    if !target_indexes_list.contains(&(indexes.clone(), line_position)) { // Why clone? Rust's compiler told me - it's because, without clone, indexes would be borrowed and dropped here, so i wouldn't be able to use it later.
        target_indexes_list.push((indexes, line_position));
        if this_num != temp_num {
            target_numbers_list.push(this_num);
            temp_num = this_num;
        }
    }
    temp_num
}


fn get_sum(file: &str) -> i32 {
    let symbols: &str  = "*@#$+-=%/&";
    let data: String   = file_parser(file);
    let lines: Vec<_>  = data.lines().collect();
    let lines_len: i32 = lines.len() as i32;

    let mut sum_list: Vec<i32> = Vec::<i32>::with_capacity(200);
    for (index_size, line) in lines.iter().enumerate() { // &&str ??????????
        let index: i32 = match index_size.try_into() {
            Ok(value) => value,
            Err(_) => {
                println!("ON LINE LOOP ->\n    Error converting `usize` to `i32`.\nJUMPING TO NEXT LINE");
                continue;
            }
        };
        let mut temp_num: i32  = 0;

        if (index+1) < lines_len && (index-1) >= 0 {
            // Getting lines: Working
            let left_size:     usize = (index - 1) as usize;
            let previous_line: &str  = lines[left_size];

            let current_line:  &str  = *line;

            let right_size:    usize = (index + 1) as usize;
            let next_line:     &str  = lines[right_size];

            // If previous_line is the first line of the input:
            if (index-1) == 0 {
                // Check if numbers on previous_line are adj to symbols on current_line:
                for (prev_line_index, line_char) in previous_line.char_indices() {
                    if line_char.is_numeric() {
                        if (
                            // Left - same line; line below:
                            (prev_line_index as i32) - 1 >= 0 &&
                            (
                                // Same line || Line below, left diagonal:
                                symbols.contains(previous_line.chars().nth(prev_line_index-1).unwrap()) ||
                                symbols.contains(current_line.chars().nth(prev_line_index-1).unwrap())
                            )
                        ) || (
                            // Same index - line below:
                            symbols.contains(current_line.chars().nth(prev_line_index).unwrap())
                        ) || (
                            // Rigth - same line; line below:
                            ((prev_line_index+1) as i32) < previous_line.len() as i32 &&
                            (
                                // Same line || Line below, right diagonal:
                                symbols.contains(previous_line.chars().nth(prev_line_index+1).unwrap()) ||
                                symbols.contains(current_line.chars().nth(prev_line_index+1).unwrap())
                            )
                        )
                        {
                            temp_num = retrieve_number(prev_line_index, previous_line, &mut sum_list,  &mut vec![(vec![1, 2], 3)], temp_num, index);
                        }
                    }
                }
            }

            // If next line is the last line of the input:
            if (index+2) == lines_len {
                // Check if numbers on next_line are adj to symbols on current_line:
                for (next_line_index, line_char) in next_line.char_indices() {
                    if line_char.is_numeric() {
                        if (
                            // Left - same line; line below:
                            (next_line_index as i32) - 1 >= 0 &&
                            (
                                // Same line || Line above, left diagonal:
                                symbols.contains(next_line.chars().nth(next_line_index-1).unwrap()) ||
                                symbols.contains(current_line.chars().nth(next_line_index-1).unwrap())
                            )
                        ) || (
                            // Same index - line above:
                            symbols.contains(current_line.chars().nth(next_line_index).unwrap())
                        ) || (
                            // Right - same line; line above:
                            ((next_line_index as i32) + 1) < previous_line.len() as i32 &&
                            (
                                symbols.contains(next_line.chars().nth(next_line_index+1).unwrap()) ||
                                symbols.contains(current_line.chars().nth(next_line_index+1).unwrap())
                            )
                        )
                        {
                            temp_num = retrieve_number(next_line_index, next_line, &mut sum_list, &mut vec![(vec![1, 2], 3)], temp_num, index);
                        }
                    }
                }
            }

            // Check if numbers on current_line are adj to symbols on previous_line or next_line:
            for (cur_line_index, line_char) in current_line.char_indices() {
                if line_char.is_numeric() {
                    if (
                        // Left - line above; same line; line below:
                        (cur_line_index as i32) - 1 >= 0 &&
                        (
                            // Line above, left diagonal || Same line || Line below, left diagonal:
                            symbols.contains(previous_line.chars().nth(cur_line_index-1).unwrap()) ||
                            symbols.contains(current_line.chars().nth(cur_line_index-1).unwrap()) ||
                            symbols.contains(next_line.chars().nth(cur_line_index-1).unwrap())
                        )
                    ) || (
                        // Same index - line above || line below:
                        symbols.contains(previous_line.chars().nth(cur_line_index).unwrap()) ||
                        symbols.contains(next_line.chars().nth(cur_line_index).unwrap())
                    ) || (
                        // Rigth - line above; same line; line below:
                        ((cur_line_index as i32) + 1) < current_line.len() as i32 &&
                        (
                            // Line above, rigth diagonal || Same line || Line below, right diagonal:
                            symbols.contains(previous_line.chars().nth(cur_line_index+1).unwrap()) ||
                            symbols.contains(current_line.chars().nth(cur_line_index+1).unwrap()) ||
                            symbols.contains(next_line.chars().nth(cur_line_index+1).unwrap())
                        )
                    )
                    {
                        temp_num = retrieve_number(cur_line_index, current_line, &mut sum_list, &mut vec![(vec![1, 2], 3)], temp_num, index);
                    }
                }
            }
        }
    }

    let mut sum: i32 = 0;
    for number in sum_list.iter() {
        sum += number;
    }
    sum
}


////////////////////////////Part 2////////////////////////////

fn get_gears(file: &str) -> i32 {
    let data: String   = file_parser(file);
    let lines: Vec<_>  = data.lines().collect();
    let lines_len: i32 = lines.len() as i32;

    let mut master_list: Vec<i32> = Vec::<i32>::with_capacity(500);

    for (index_size, line) in lines.iter().enumerate() { // &&str ??????????
        let index: i32 = match index_size.try_into() {
            Ok(value) => value,
            Err(_) => {
                println!("ON LINE LOOP ->\n    Error converting `usize` to `i32`.\nJUMPING TO NEXT LINE");
                continue;
            }
        };
        let mut temp_num: i32  = 0;

        if (index+1) < lines_len && (index-1) >= 0 {
            // Getting lines: Working
            let left_size:     usize = (index - 1) as usize;
            let previous_line: &str  = lines[left_size];

            let current_line:  &str  = *line;

            let right_size:    usize = (index + 1) as usize;
            let next_line:     &str  = lines[right_size];

            // If previous_line is the first line of the input:
            if (index-1) == 0 {
                if previous_line.contains('*') {
                    // Check if * on previous_line are adj to 2 numbers on current_line:
                    for (prev_line_index, gear) in previous_line.char_indices() {
                        let mut first_line_nums   : Vec<i32>             = vec![];
                        let mut first_line_indexes: Vec<(Vec<i32>, i32)> = vec![];

                        if gear == '*' {
                            // Left - same line; line below:
                            if (prev_line_index as i32-1) >= 0 {
                                // Same line:
                                if previous_line.chars().nth(prev_line_index-1).unwrap().is_numeric() {
                                    temp_num = retrieve_number(
                                        prev_line_index-1,
                                        previous_line,
                                        &mut first_line_nums,
                                        &mut first_line_indexes,
                                        temp_num,
                                        index
                                    );
                                }
                                // Line below, left diagonal:
                                if current_line.chars().nth(prev_line_index-1).unwrap().is_numeric() {
                                    temp_num = retrieve_number(
                                        prev_line_index-1,
                                        current_line,
                                        &mut first_line_nums,
                                        &mut first_line_indexes,
                                        temp_num,
                                        index+1
                                    );
                                }
                            }

                            // Same index - line below:
                            if current_line.chars().nth(prev_line_index).unwrap().is_numeric() {
                                temp_num = retrieve_number(
                                    prev_line_index,
                                    current_line,
                                    &mut first_line_nums,
                                    &mut first_line_indexes,
                                    temp_num,
                                    index+1
                                );
                            }

                            // Rigth - same line; line below:
                            if (prev_line_index - 1) < previous_line.len() {
                                // Same line:
                                if previous_line.chars().nth(prev_line_index+1).unwrap().is_numeric() {
                                    temp_num = retrieve_number(
                                        prev_line_index+1,
                                        previous_line,
                                        &mut first_line_nums,
                                        &mut first_line_indexes,
                                        temp_num,
                                        index
                                    );
                                }
                                // Line below, right diagonal:
                                if current_line.chars().nth(prev_line_index+1).unwrap().is_numeric() {
                                    temp_num = retrieve_number(
                                        prev_line_index+1,
                                        current_line,
                                        &mut first_line_nums,
                                        &mut first_line_indexes,
                                        temp_num,
                                        index+1
                                    );
                                }
                            }
                        }

                        // If there are exactly 2 numbers adjacent to '*':
                        if first_line_nums.len() == 2 {
                            master_list.push(first_line_nums[0]*first_line_nums[1])
                        }
                    }
                }
            }

            // If next line is the last of the input:
            if (index+2) == lines_len {
                if next_line.contains('*') {
                    // Check if numbers on next_line are adj to symbols on current_line:
                    for (next_line_index, gear) in next_line.char_indices() {
                        let mut last_line_nums   : Vec<i32>             = vec![];
                        let mut last_line_indexes: Vec<(Vec<i32>, i32)> = vec![];

                        if gear == '*' {
                            // Left - same line || line above:
                            if (next_line_index as i32 - 1) >= 0 {
                                // Same line:
                                if next_line.chars().nth(next_line_index-1).unwrap().is_numeric() {
                                    temp_num = retrieve_number(
                                        next_line_index-1,
                                        next_line,
                                        &mut last_line_nums,
                                        &mut last_line_indexes,
                                        temp_num,
                                        index
                                    );
                                }
                                // Line above, left diagonal:
                                if next_line.chars().nth(next_line_index-1).unwrap().is_numeric() {
                                    temp_num = retrieve_number(
                                        next_line_index-1,
                                        current_line,
                                        &mut last_line_nums,
                                        &mut last_line_indexes,
                                        temp_num,
                                        index-1
                                    );
                                }
                            }

                            // Same index - line above:
                            if current_line.chars().nth(next_line_index).unwrap().is_numeric() {
                                temp_num = retrieve_number(
                                    next_line_index,
                                    current_line,
                                    &mut last_line_nums,
                                    &mut last_line_indexes,
                                    temp_num,
                                    index-1
                                );
                            }

                            // Rigth - same line || line above:
                            if (next_line_index + 1) < previous_line.len() {
                                // Same line:
                                if next_line.chars().nth(next_line_index+1).unwrap().is_numeric() {
                                    temp_num = retrieve_number(
                                        next_line_index+1,
                                        next_line,
                                        &mut last_line_nums,
                                        &mut last_line_indexes,
                                        temp_num,
                                        index
                                    );
                                }
                                // Line above, right diagonal:
                                if current_line.chars().nth(next_line_index+1).unwrap().is_numeric() {
                                    temp_num = retrieve_number(
                                        next_line_index+1,
                                        current_line,
                                        &mut last_line_nums,
                                        &mut last_line_indexes,
                                        temp_num,
                                        index-1
                                    );
                                }
                            }
                        }

                        // If there are exactly 2 numbers adjacent to '*':
                        if last_line_nums.len() == 2 {
                            master_list.push(last_line_nums[0]*last_line_nums[1]);
                        }
                    }
                }
            }

            if current_line.contains('*') {
                // Check if numbers on current_line are adj to symbols on previous_line or next_line:
                for (cur_line_index, gear) in current_line.char_indices() {
                    let mut cur_line_nums   : Vec<i32>             = vec![];
                    let mut cur_line_indexes: Vec<(Vec<i32>, i32)> = vec![];

                    if gear == '*' {
                        // Left - line above; same line; line below:
                        if (cur_line_index as i32 - 1) >= 0 {
                            // Line above, left diagonal:
                            if previous_line.chars().nth(cur_line_index-1).unwrap().is_numeric() {
                                temp_num = retrieve_number(
                                    cur_line_index-1,
                                    previous_line,
                                    &mut cur_line_nums,
                                    &mut cur_line_indexes,
                                    temp_num,
                                    index-1
                                );
                            }
                            // Same line
                            if current_line.chars().nth(cur_line_index-1).unwrap().is_numeric() {
                                temp_num = retrieve_number(
                                    cur_line_index-1,
                                    current_line,
                                    &mut cur_line_nums,
                                    &mut cur_line_indexes,
                                    temp_num,
                                    index
                                );
                            }
                            // Line below, left diagonal:
                            if next_line.chars().nth(cur_line_index-1).unwrap().is_numeric() {
                                temp_num = retrieve_number(
                                    cur_line_index-1,
                                    next_line,
                                    &mut cur_line_nums,
                                    &mut cur_line_indexes,
                                    temp_num,
                                    index+1
                                );
                            }
                        }

                        // Same index - line above:
                        if previous_line.chars().nth(cur_line_index).unwrap().is_numeric() {
                            temp_num = retrieve_number(
                                cur_line_index,
                                previous_line,
                                &mut cur_line_nums,
                                &mut cur_line_indexes,
                                temp_num,
                                index-1
                            );
                        }
                        // Same index - line below:
                        if next_line.chars().nth(cur_line_index).unwrap().is_numeric() {
                            temp_num = retrieve_number(
                                cur_line_index,
                                next_line,
                                &mut cur_line_nums,
                                &mut cur_line_indexes,
                                temp_num,
                                index+1
                            );
                        }

                        // Rigth - line above; same line; line below:
                        if (cur_line_index + 1) < current_line.len() {
                            // Line above, rigth diagonal:
                            if previous_line.chars().nth(cur_line_index+1).unwrap().is_numeric() {
                                temp_num = retrieve_number(
                                    cur_line_index+1,
                                    previous_line,
                                    &mut cur_line_nums,
                                    &mut cur_line_indexes,
                                    temp_num,
                                    index-1
                                );
                            }
                            // Same line:
                            if current_line.chars().nth(cur_line_index+1).unwrap().is_numeric() {
                                temp_num = retrieve_number(
                                    cur_line_index+1,
                                    current_line,
                                    &mut cur_line_nums,
                                    &mut cur_line_indexes,
                                    temp_num,
                                    index
                                );
                            }
                            // Line below, right diagonal:
                            if next_line.chars().nth(cur_line_index+1).unwrap().is_numeric() {
                                temp_num = retrieve_number(
                                    cur_line_index+1,
                                    next_line,
                                    &mut cur_line_nums,
                                    &mut cur_line_indexes,
                                    temp_num,
                                    index+1
                                );
                            }
                        }
                    }

                    // If there's exactly 2 numbers adjacent to '*':
                    if cur_line_nums.len() == 2 {
                        master_list.push(cur_line_nums[0]*cur_line_nums[1]);
                    }
                }
            }
        }
    }

    let mut sum: i32 = 0;
    for number in master_list.iter() {
        sum += number;
    }
    sum
}


////////// Unit Tests //////////
#[cfg(test)]
mod unit_tests {
    #[test]
    fn get_sum_from_test() {
        assert_eq!(super::get_sum("src/test.txt"), 4361i32);
    }
    #[test]
    fn get_sum_from_schematic() {
        assert_eq!(super::get_sum("src/schematic.txt"), 539590i32);
    }

    #[test]
    fn get_gears_from_test() {
        assert_eq!(super::get_gears("src/test.txt"), 467835i32);
    }
    #[test]
    fn get_gears_from_schematic() {
        assert_eq!(super::get_gears("src/schematic.txt"), 80703636i32);
    }
}
