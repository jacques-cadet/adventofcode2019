INPUT_FILE = 'day002.txt'


def create_program(source, noun, verb):
    program = source.copy()
    program[1] = noun
    program[2] = verb
    return program


def run_intcode(code_list):
    ip = 0
    while True:
        opcode = code_list[ip]
        if opcode == 99:
            break
        if opcode in (1, 2):
            op, pos1, pos2, resultpos = code_list[ip:ip+4]
            val1, val2 = code_list[pos1], code_list[pos2]
            result = val1 * val2 if op == 2 else val1 + val2
            code_list[resultpos] = result
        ip += 4


def part1(filename):
    with open(filename) as f:
        source_string = f.read().strip()
        source = [int(i) for i in source_string.split(',')]
        program = create_program(source, noun=12, verb=2)
        run_intcode(program)
        return program[0]


def part2(filename):
    with open(filename) as f:
        source_string = f.read().strip()
        source = [int(i) for i in source_string.split(',')]
        # Param generator
        params = ((noun, verb) for noun in range(100) for verb in range(100))
        for noun, verb in params:
            program = create_program(source, noun, verb)
            run_intcode(program)
            result = program[0]
            if result == 19690720:
                return 100 * noun + verb


if __name__ == '__main__':
    print('Part 1:', part1(INPUT_FILE))
    print('Part 2:', part2(INPUT_FILE))

