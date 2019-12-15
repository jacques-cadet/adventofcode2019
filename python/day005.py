import intcode

INPUT_FILE = 'day005.in'


def part1(filename):
    source = intcode.load_from_file(filename)
    i, o = [], []
    # AC Unit input value
    i.append(1)
    modified = intcode.run_intcode(source, i, o)
    return modified[0], i, o


def part2(filename):
    source = intcode.load_from_file(filename)
    i, o = [], []
    # Thermal Radiator Controller
    i.append(5)
    modified = intcode.run_intcode(source, i, o)
    return modified[0], i, o


if __name__ == '__main__':
    result_code, instream, outstream = part1(INPUT_FILE)
    print('Part1: ', result_code, 'IN', instream, 'OUT', outstream)
    result_code, instream, outstream = part2(INPUT_FILE)
    print('Part2: ', result_code, 'IN', instream, 'OUT', outstream)
