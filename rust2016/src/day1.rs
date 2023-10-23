use crate::loadfile::filereader;

use std::collections::HashSet;

pub fn day1_entry() {
    println!("More stuff!");

    let my_input = filereader("./data/day1.txt");

    println!("Compute D1: {}", day1p1_compute(&my_input));
    println!("Compute D2: {}", day1p2_compute(&my_input));
}

fn day1p1_compute(data: &String) -> i32 {
    
    let moves = data.split(", ");
    let mut dir = Dir::North;

    let mut x: i32 = 0;
    let mut y: i32 = 0;

    for mv in moves {
        let turn = mv.chars().take(1).last().unwrap();
        let i = &mv[1..].parse::<i32>().unwrap();
        match turn {
            'R' => dir = turn_right(&dir),
            'L' => dir = turn_left(&dir),
            _  => panic!()
        }
        match dir {
            Dir::North => y += i,
            Dir::East => x += i,
            Dir::South => y -= i,
            Dir::West => x -= i 
        }
    }

    x.abs() + y.abs()
}

fn day1p2_compute(data: &String) -> i32 {
    
    let moves = data.split(", ");
    let mut dir = Dir::North;

    let mut x: i32 = 0;
    let mut y: i32 = 0;

    let mut visited = HashSet::new();

    'outer: for mv in moves {
        let turn = mv.chars().take(1).last().unwrap();
        let i = &mv[1..].parse::<i32>().unwrap();
        match turn {
            'R' => dir = turn_right(&dir),
            'L' => dir = turn_left(&dir),
            _  => panic!()
        }
        for _ in 0..*i {
            match dir {
                Dir::North => y += 1,
                Dir::East => x += 1,
                Dir::South => y -= 1,
                Dir::West => x -= 1 
            }
            if visited.contains(&(x, y)) {
                break 'outer;
            } else {
                visited.insert((x, y));
            }
        }
    }

    x.abs() + y.abs()
}

fn turn_right(dir: &Dir) -> Dir {
    match dir {
        Dir::North => Dir::East,
        Dir::East => Dir::South,
        Dir::South => Dir::West,
        Dir::West => Dir::North
    }
}

fn turn_left(dir: &Dir) -> Dir {
    match dir {
        Dir::North => Dir::West,
        Dir::East => Dir::North,
        Dir::South => Dir::East,
        Dir::West => Dir::South
    }
}

enum Dir {
    North,
    South,
    East,
    West
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test() {
        assert_eq!(day1p1_compute(&"R2, L3".to_string()), 5);
        assert_eq!(day1p1_compute(&"R2, R2, R2".to_string()), 2);
        assert_eq!(day1p1_compute(&"R5, L5, R5, R3".to_string()), 12);
    }

    #[test]
    fn test2() {
        assert_eq!(day1p2_compute(&"R8, R4, R4, R8".to_string()), 4);
    }
}
