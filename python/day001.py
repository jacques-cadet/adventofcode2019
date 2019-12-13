INPUT_FILE = 'day001.in'


def calculate_fuel(mass):
    fuel = mass // 3 - 2
    total = 0
    while fuel > 0:
        total += fuel
        fuel = fuel // 3 - 2
    return total


def part1(filename):
    with open(filename) as f:
        return sum([int(m.strip()) // 3 - 2 for m in f])


def part2(filename):
    with open(filename) as f:
        return sum([calculate_fuel(int(m.strip())) for m in f])


if __name__ == '__main__':
    print('Part 1:', part1(INPUT_FILE))
    print('Part 2:', part2(INPUT_FILE))
