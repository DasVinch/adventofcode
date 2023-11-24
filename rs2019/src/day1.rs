use crate::loadfile::filereader;

pub fn day1_entry() {
    println!("More stuff!");

    let my_input = filereader("../inputs/2019/input1.txt");
    let int_vec: Vec<i32> = parser(&my_input);

    println!("Compute D1: {}", day1p1_compute(&int_vec));
    println!("Compute D2: {}", day1p2_compute(&int_vec));
}

fn parser(input_text: &str) -> Vec<i32> {
    let mut vec_num = Vec::<i32>::new();
    for line in input_text.lines() {
        if !line.is_empty() {
            vec_num.push(line.parse::<i32>().unwrap());
        }
    }
    vec_num
}

fn fuel_req(mass: i32) -> i32 {
    let fuel = mass / 3 - 2;
    if fuel < 0 {
        return 0;
    }
    fuel
}

fn day1p1_compute(data: &Vec<i32>) -> i32 {
    let mut total: i32 = 0;
    for mass in data {
        total += fuel_req(*mass);
    }
    total
}

fn fuel_req_p2(mass: i32) -> i32 {
    let mut fuel = mass / 3 - 2;
    let mut fuelmass = fuel;
    while fuelmass > 0 {
        fuelmass = fuel_req(fuelmass);
        fuel += fuelmass
    }
    fuel
}

fn day1p2_compute(data: &Vec<i32>) -> i32 {
    data.iter().map(|x| fuel_req_p2(*x)).sum()
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test() {
        assert_eq!(fuel_req(12), 2);
        assert_eq!(fuel_req(14), 2);
        assert_eq!(fuel_req(1969), 654);
        assert_eq!(fuel_req(100756), 33583);
    }

    #[test]
    fn test2() {
        assert_eq!(fuel_req_p2(14), 2);
        assert_eq!(fuel_req_p2(1969), 966);
        assert_eq!(fuel_req_p2(100756), 50346);
    }
}
