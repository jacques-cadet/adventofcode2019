"""Intcode Computer interpreter, for puzzles on day 5 and later"""
import operator
from collections import namedtuple

Instruction = namedtuple('Instruction', 'opcode name params function')


def param_value(param, mode, memory):
    return param if mode == 1 else memory[param]


def add(param1, param2, result_pos,
        memory=None, instream=None, outstream=None):
    val1 = param_value(*param1, memory)
    val2 = param_value(*param2, memory)
    if result_pos[1] != 0:
        raise ValueError('ADDN param 3 must use reference mode')
    print('(', val1, '+', val2, '=', val1 + val2, ' => @', result_pos[0], ')', sep='')
    memory[result_pos[0]] = val1 + val2


def multiply(param1, param2, result_pos,
             memory=None, instream=None, outstream=None):
    val1 = param_value(*param1, memory)
    val2 = param_value(*param2, memory)
    if result_pos[1] != 0:
        raise ValueError('MULT param 3 must use reference mode')
    print('(', val1, '*', val2, '=', val1 * val2, ' => @', result_pos[0], ')', sep='')
    memory[result_pos[0]] = val1 * val2


def pop_input(store_pos,
              memory=None, instream=None, outstream=None):
    if store_pos[1] != 0:
        raise ValueError('INPT param must use reference mode')
    memory[store_pos[0]] = instream.pop(0)


def push_output(param1,
                memory=None, instream=None, outstream=None):
    val1 = param_value(*param1, memory)
    outstream.append(val1)


def jump_true(param1, param2,
              memory=None, instream=None, outstream=None):
    test_value = param_value(*param1, memory)
    jump_pos = param_value(*param2, memory)
    return jump_pos if test_value else None


def jump_false(param1, param2,
               memory=None, instream=None, outstream=None):
    test_value = param_value(*param1, memory)
    jump_pos = param_value(*param2, memory)
    return jump_pos if not test_value else None


def less_than(param1, param2, result_pos,
              memory=None, instream=None, outstream=None):
    val1 = param_value(*param1, memory)
    val2 = param_value(*param2, memory)
    if result_pos[1] != 0:
        raise ValueError('LESS param 3 must use reference mode')
    print('(', val1, '<', val2, '=', val1 < val2, ' => @', result_pos[0], ')', sep='')
    memory[result_pos[0]] = 1 if val1 < val2 else 0


def equals(param1, param2, result_pos,
           memory=None, instream=None, outstream=None):
    val1 = param_value(*param1, memory)
    val2 = param_value(*param2, memory)
    if result_pos[1] != 0:
        raise ValueError('EQUL param 3 must use reference mode')
    print('(', val1, '==', val2, '=', val1 < val2, ' => @', result_pos[0], ')', sep='')
    memory[result_pos[0]] = 1 if val1 == val2 else 0


def halt_program(memory=None, instream=None, outstream=None):
    raise RuntimeError('Program Halted')


OPCODE_LOOKUP = {
    1: Instruction(opcode=1, name='ADDN', params=3, function=add),
    2: Instruction(opcode=2, name='MULT', params=3, function=multiply),
    3: Instruction(opcode=3, name='INPT', params=1, function=pop_input),
    4: Instruction(opcode=4, name='OUTP', params=1, function=push_output),
    5: Instruction(opcode=5, name='JMPT', params=2, function=jump_true),
    6: Instruction(opcode=6, name='JMPF', params=2, function=jump_false),
    7: Instruction(opcode=7, name='LESS', params=3, function=less_than),
    8: Instruction(opcode=8, name='EQUL', params=3, function=equals),
    99: Instruction(opcode=99, name='HALT', params=0, function=halt_program),
}

PARAM_MODE_PREFIX = {
    0: '@',
    1: '',
}


def debug_log(instruction, params):
    print(f'[{instruction.opcode:02d}] {instruction.name}', end=' ')
    print(*[PARAM_MODE_PREFIX.get(p[1], '') + str(p[0]) for p in params], end=' ')
    if instruction.opcode not in (1, 2, 7, 8):
        print()


def read_opcode(op_value):
    # Ignore the two rightmost digits
    param_modes, opcode = divmod(op_value, 100)
    return opcode, param_modes


def get_parameter_modes(modeflags, params):
    places = [10 ** x for x in range(params)]
    flags = [modeflags // p % 10 for p in places]
    return flags


def execute_instruction(
        instruction, modeflags, memory, ip,
        instream=None, outstream=None):
    param_modes = (
        get_parameter_modes(modeflags, instruction.params)
        if instruction.params else [])
    op_params = memory[ip+1:ip+instruction.params+1]
    params = list(zip(op_params, param_modes))
    debug_log(instruction, params)
    return instruction.function(
        *params,
        memory=memory,
        instream=instream,
        outstream=outstream)


def run_intcode(program, instream=None, outstream=None):
    ip = 0
    while True:
        opcode, mode = read_opcode(program[ip])
        try:
            instruction = OPCODE_LOOKUP[opcode]
            jump_pos = execute_instruction(
                instruction, mode, program, ip,
                instream=instream, outstream=outstream)
        except RuntimeError:
            break
        if jump_pos is not None:
            ip = jump_pos
        else:
            ip += instruction.params + 1
    print('Program Halted.')
    return program


def load_from_file(filename):
    with open(filename) as f:
        source_string = f.read().strip()
        source = [int(i) for i in source_string.split(',')]
    return source
