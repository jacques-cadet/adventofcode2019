INPUT_FILE = 'day003.in'
DELTAS = {
    'U': (0, 1),
    'D': (0, -1),
    'R': (1, 0),
    'L': (-1, 0),
}


def generate_point_set(wire_path):
    # Central port
    x, y = 0, 0
    wire_points = dict()
    wire_distance = 0
    for span in wire_path:
        x_delta, y_delta = DELTAS[span[0]]
        span_len = int(span[1:])
        for i in range(span_len):
            x += x_delta
            y += y_delta
            wire_distance += 1
            wire_points.setdefault((x, y), wire_distance)
    return wire_points


def manhattan_distance(x, y):
    return abs(x) + abs(y)


def part1(filename):
    wires = []
    with open(filename) as f:
        for line in f:
            path = line.split(',')
            wires.append(generate_point_set(path))
    cross_points = set.intersection(*[set(wire) for wire in wires])
    return min([manhattan_distance(c[0], c[1]) for c in cross_points])


def part2(filename):
    wires = []
    with open(filename) as f:
        for line in f:
            path = line.split(',')
            wires.append(generate_point_set(path))
    cross_points = set.intersection(*[set(wire) for wire in wires])
    return min([sum([w[point] for w in wires]) for point in cross_points])


if __name__ == '__main__':
    print('Part 1:', part1(INPUT_FILE))
    print('Part 2:', part2(INPUT_FILE))
