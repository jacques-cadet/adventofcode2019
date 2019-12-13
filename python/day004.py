INPUT_RANGE = '134564-585159'


def validate_password(value, digits=None, min_span=None, exact_span=None):
    digits = digits or 6
    modvalue = 10 ** (digits - 1)
    prev_quotient = 0
    spans = []
    span_length = 0
    while modvalue >= 1:
        quotient, value = divmod(value, modvalue)
        if quotient < prev_quotient:
            return False
        if span_length and quotient != prev_quotient:
            spans.append(span_length)
            span_length = 0
        span_length += 1
        prev_quotient = quotient
        modvalue /= 10
    spans.append(span_length)
    if exact_span and not [s for s in spans if s == exact_span]:
        return False
    if min_span and not [s for s in spans if s >= min_span]:
        return False

    return True


def part1(range_string):
    start, end = [int(r) for r in range_string.split('-')]
    good_passwords = [
        p for p in range(start, end)
        if validate_password(p, digits=6, min_span=2)]
    return len(good_passwords)


def part2(range_string):
    start, end = [int(r) for r in range_string.split('-')]
    good_passwords = [
        p for p in range(start, end)
        if validate_password(p, digits=6, exact_span=2)]
    return len(good_passwords)


if __name__ == '__main__':
    print('Part 1:', part1(INPUT_RANGE))
    print('Part 2:', part2(INPUT_RANGE))

