use crate::loadfile::filereader;

#[derive(Debug)]
enum Dir {
    U,
    R,
    L,
    D
}

impl Dir {
    fn parse_char(c: char) -> Self {
        match c {
            'U' => return Dir::U,
            'R' => return Dir::R,
            'L' => return Dir::L,
            'D' => return Dir::D,
            _ => panic!()
        }
    }
}

#[derive(Debug)]
struct Segment {
    a: (i32, i32),
    b: (i32, i32)
}

pub fn entry() {
    println!("Running day 3!");

    let my_input = filereader("../inputs/2019/input3.txt");
    let vec_pair = parser(&my_input);

    //println!("{}", int_vec.len());

    //println!("Compute P1: {}", p1_compute(&int_vec));
    //println!("Compute P2: {}", p2_compute(&int_vec));
}

fn parser(input_text: &str) -> (Vec<Segment>, Vec<Segment>) {
    let mut parts = input_text.lines();
    return (segmentize_wire(&parse_wire(parts.next().unwrap())),
            segmentize_wire(&parse_wire(parts.next().unwrap())))
}

fn parse_wire(single_line: &str) -> Vec<(Dir, i32)> {
    let parts = single_line.split(",");
    let mut vec_num = Vec::<(Dir, i32)>::new();
    for m in parts {
        let dir = Dir::parse_char(m.chars().next().unwrap());
        match m[1..].parse::<i32>() {
            Ok(x) => vec_num.push((dir, x)),
            _ => (),
        }
        
    }
    vec_num
}

fn segmentize_wire(parsed_wire: &[(Dir, i32)]) -> Vec<Segment> {
    let mut vec_seg = Vec::<Segment>::new();
    let mut last_point = (0,0);
    for (d, len) in parsed_wire {
        vec_seg.push(make_segment(d, *len, last_point));
        last_point = vec_seg.last().expect("empty vec_seg").b;
    }
    vec_seg
}

fn make_segment(dir: &Dir, len: i32, origin: (i32, i32)) -> Segment {
    // compute destination, create segment.
    match dir {
        Dir::U => return Segment {a:origin, b:(origin.0, origin.1 + len)},
        Dir::L => return Segment {a:origin, b:(origin.0 - len, origin.1)},
        Dir::R => return Segment {a:origin, b:(origin.0 + len, origin.1)},
        Dir::D => return Segment {a:origin, b:(origin.0, origin.1 - len)}
    }
}

fn segment_intersects(s1: Segment, s2: Segment) -> Option<(i32, i32)> {
    // Doesn't support multi-overlap, will return just one square of overlap.
    if s1.a.0 == s1.b.0 { // s1 vertical
        if s2.a.0 == s2.b.0 { // s2 vertical
            if s1.a.0 != s2.a.0 { // different column.
                return None;
            }
            // Same column
            if ... { // has overlap 

            }
            return None
        } else { // s2 horizontal

        }
    } else { // s1 horizontal

    }
}

fn p1_compute(data: &Vec<usize>) -> usize {
    unimplemented!();
}

fn p2_compute(data: &Vec<usize>) -> usize {
    unimplemented!();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test() {
        println!("{:?}", parser(&"R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"));
    }

    #[test]
    fn test2() {
    }
}
