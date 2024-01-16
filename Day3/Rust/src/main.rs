fn main() {
    println!("Test: {}", get_sum("src/test.txt"));
    assert_eq!(get_sum("src/test.txt"), 4361i32);
    println!("Input: {}", get_sum("src/schematic.txt"));
    assert_eq!(get_sum("src/schematic.txt"), 539590i32);
}


use std::fs;
fn file_parser(file: &str) -> String {
    let data: String = fs::read_to_string(file).expect("Unable to read file.");
    data
}


/// Getting number at specified index: Working
fn get_number(initial_index: usize, line: &str) -> i32 {
    let mut the_number: String = String::from("");

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
    the_number.parse::<i32>().unwrap()
}


fn retrieve_number(
    line_index: usize, target_line: &str, target_list: &mut Vec<i32>, mut temp_num: i32
) -> i32 {
    let this_num: i32 = get_number(line_index, target_line);
    if this_num != temp_num {
        target_list.push(this_num);
        temp_num = this_num;
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
                        // I'm not sure if this is better or worse than sepparating the `ìf`s.
                        // Leaving the second option as comments just so i remember
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
                            temp_num = retrieve_number(prev_line_index, previous_line, &mut sum_list, temp_num);
                        }

                        // Left - same line; line below:
                        // if ((prev_line_index as i32) - 1) >= 0 { // If ther's a char on the left
                        //     // Same line || Line below, left diagonal:
                        //     if symbols.contains(previous_line.chars().nth(prev_line_index-1).unwrap())
                        //     || symbols.contains(current_line.chars().nth(prev_line_index-1).unwrap())
                        //     {
                        //         temp_num = retrieve_number(prev_line_index, previous_line, &mut sum_list, temp_num);
                        //     }
                        // }

                        // Same index - line below:
                        // if symbols.contains(current_line.chars().nth(prev_line_index).unwrap()) {
                        //     temp_num = retrieve_number(prev_line_index, previous_line, &mut sum_list, temp_num);
                        // }

                        // Rigth - same line; line below:
                        // if ((prev_line_index+1) as i32) < previous_line.len() as i32 {
                        //     // Same line || Line below, right diagonal:
                        //     if symbols.contains(previous_line.chars().nth(prev_line_index+1).unwrap())
                        //     || symbols.contains(current_line.chars().nth(prev_line_index+1).unwrap())
                        //     {
                        //         temp_num = retrieve_number(prev_line_index, previous_line, &mut sum_list, temp_num);
                        //     }
                        // }
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
                            temp_num = retrieve_number(next_line_index, next_line, &mut sum_list, temp_num);
                        }

                        // Left - same line; line below:
                        // if ((next_line_index as i32) - 1) >= 0 {
                            // Same line || Line above, left diagonal:
                        //     if symbols.contains(next_line.chars().nth(next_line_index-1).unwrap())
                        //     || symbols.contains(current_line.chars().nth(next_line_index-1).unwrap())
                        //     {
                        //         temp_num = retrieve_number(next_line_index, next_line, &mut sum_list, temp_num);
                        //     }
                        // }

                        // Same index - line above:
                        // if symbols.contains(current_line.chars().nth(next_line_index).unwrap()) {
                        //     temp_num = retrieve_number(next_line_index, next_line, &mut sum_list, temp_num);
                        // }

                        // Right - same line; line above:
                        // if ((next_line_index as i32) + 1) < previous_line.len() as i32 {
                        //     // Same line || Line above, right diagonal:
                        //     if symbols.contains(next_line.chars().nth(next_line_index+1).unwrap())
                        //     || symbols.contains(current_line.chars().nth(next_line_index+1).unwrap())
                        //     {
                        //         temp_num = retrieve_number(next_line_index, next_line, &mut sum_list, temp_num);
                        //     }
                        // }
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
                        temp_num = retrieve_number(cur_line_index, current_line, &mut sum_list, temp_num);
                    }

                    // Left - line above; same line; line below:
                    // if ((cur_line_index as i32) - 1) >= 0 {
                    //     // Line above, left diagonal || Same line || Line below, left diagonal:
                    //     if symbols.contains(previous_line.chars().nth(cur_line_index-1).unwrap())
                    //     || symbols.contains(current_line.chars().nth(cur_line_index-1).unwrap())
                    //     || symbols.contains(next_line.chars().nth(cur_line_index-1).unwrap())
                    //     {
                    //         temp_num = retrieve_number(cur_line_index, current_line, &mut sum_list, temp_num);
                    //     }
                    // }

                    // Same index - line above || line below:
                    // if symbols.contains(previous_line.chars().nth(cur_line_index).unwrap())
                    // || symbols.contains(next_line.chars().nth(cur_line_index).unwrap())
                    // {
                    //     temp_num = retrieve_number(cur_line_index, current_line, &mut sum_list, temp_num);
                    // }

                    // Rigth - line above; same line; line below:
                    // if ((cur_line_index as i32) + 1) < current_line.len() as i32 {
                    //     // Line above, rigth diagonal || Same line || Line below, right diagonal:
                    //     if symbols.contains(previous_line.chars().nth(cur_line_index+1).unwrap())
                    //     || symbols.contains(current_line.chars().nth(cur_line_index+1).unwrap())
                    //     || symbols.contains(next_line.chars().nth(cur_line_index+1).unwrap())
                    //     {
                    //         temp_num = retrieve_number(cur_line_index, current_line, &mut sum_list, temp_num);
                    //     }
                    // }
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



////////// Unit Tests //////////
#[cfg(test)]
mod unit_tests {
    #[test]
    fn get_gears_from_test() {
        assert_eq!(super::get_sum("src/test.txt"), 4361i32);
    }
    #[test]
    fn get_gears_from_schematic() {
        assert_eq!(super::get_sum("src/schematic.txt"), 539590i32);
    }
}
