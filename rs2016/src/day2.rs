use crate::loadfile::filereader;

pub fn day2_entry() {
    println!("More stuff!");

    let my_input = filereader("./data/day2.txt");

    println!("Compute D1: {}", day2p1_compute(&my_input));
    println!("Compute D2: {}", day2p2_compute(&my_input));
}

fn day2p1_compute(data: &String) -> String {
    "YOLO".to_string()
}

fn day2p2_compute(data: &String) -> String {
    "SWAG".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test() {
        assert_eq!(day2p1_compute(&"ULL\nRRDDD\nLURDL\nUUUUD".to_string()), "1985");
    }

    #[test]
    fn test2() {
    }
}
