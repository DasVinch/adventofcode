use crate::loadfile::filereader;

pub fn day2_entry() {
    println!("Running day 2!");

    let my_input = filereader("../inputs/2019/input2.txt");
    let int_vec = parser(&my_input);

    println!("{}", int_vec.len());

    println!("Compute P1: {}", p1_compute(&int_vec));
    println!("Compute P2: {}", p2_compute(&int_vec));
}

fn parser(input_text: &str) -> Vec<usize> {
    let parts = input_text.split(",");
    let mut vec_num = Vec::<usize>::new();
    for m in parts {
        match m.parse::<usize>() {
            Ok(x) => vec_num.push(x),
            _ => (),
        }
        
    }
    vec_num
}

fn p1_compute(data: &Vec<usize>) -> usize {
    let mut data_copy = data.clone();
    // Special rules
    data_copy[1] = 12;
    data_copy[2] = 2;

    execute(&mut data_copy);

    data_copy[0]
}

fn p2_compute(data: &Vec<usize>) -> usize {
    for a in 0..100 {
        for b in 0..100 {
            let mut data_copy = data.clone();
            data_copy[1] = a;
            data_copy[2] = b;

            execute(&mut data_copy);

            if data_copy[0] == 19690720 {
                return 100*a + b;
            }
        }
    }
    panic!("Not found!");
}

fn execute(memory: &mut [usize]) -> () {
    let mut i_ptr: usize = 0;
    while memory[i_ptr] != 99 {
        intcode_instr_apply(i_ptr, memory);
        i_ptr += 4;
    }
}

fn intcode_instr_apply(i_ptr: usize, ribbon: &mut [usize]) {
    let opcode = ribbon[i_ptr];
    let op1 = ribbon[i_ptr + 1];
    let op2 = ribbon[i_ptr + 2];
    let dest = ribbon[i_ptr + 3];
    match opcode {
        1 => ribbon[dest] = ribbon[op1] + ribbon[op2],
        2 => ribbon[dest] = ribbon[op1] * ribbon[op2],
        _ => {
            panic!("Bad bad 99.")
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test() {
        let v = &mut parser("1,0,0,0,99"); 
        execute(v);
        assert_eq!(v[0], 2);
        let v = &mut parser("2,3,0,3,99"); 
        execute(v);
        assert_eq!(v[0], 2);
        let v = &mut parser("1,1,1,4,99,5,6,0,99"); 
        execute(v);
        assert_eq!(v[0], 30);
    }

    #[test]
    fn test2() {
        assert_eq!(0, 0);
    }
}
