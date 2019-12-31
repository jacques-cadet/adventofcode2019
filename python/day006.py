INPUT_FILE = 'day006.in'


class TreeDict(dict):
    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent', None)
        self.name = kwargs.pop('name', None)
        super().__init__(*args, **kwargs)


def process_orbits(orbit_pairs):
    orbit_index = {}
    for center, body in orbit_pairs:
        center_orbits = orbit_index.setdefault(center, TreeDict(name=center))
        print('Current orbits for', center, center_orbits.keys())
        body_orbits = orbit_index.setdefault(body, TreeDict(name=body))
        print('Current orbits for', body, body_orbits.keys())
        center_orbits[body] = body_orbits
        body_orbits.parent = center_orbits
    return orbit_index


def print_orbits(orbit_tree):
    print('->', list(orbit_tree.keys()))
    for key in orbit_tree:
        print(key, end='')
        print_orbits(orbit_tree[key])


def find_depth(orbit_index, key):
    depth = 0
    body = orbit_index[key]
    while body.parent:
        depth += 1
        body = body.parent
    return depth


def path_to_root(orbit_index, body):
    path = [body.name]
    while body.parent:
        body = body.parent
        path.append(body.name)
    return path


def path_to_body(orbit_index, start, end):
    start_body = orbit_index[start]
    end_body = orbit_index[end]

    start_to_root = path_to_root(orbit_index, start_body)
    print('Start to root:', start_to_root)
    end_to_root = path_to_root(orbit_index, end_body)
    print('End to root:', end_to_root)
    for ancestor in start_to_root:
        if ancestor in end_to_root:
            break
    print('Found common ancestor:', ancestor)
    root_to_end = list(reversed(end_to_root))
    path = (
        start_to_root[:start_to_root.index(ancestor)] +
        root_to_end[root_to_end.index(ancestor):])
    return path


def part1(filename):
    with open(filename) as f:
        orbit_pairs = [line.strip().split(')') for line in f]
    orbit_tree = process_orbits(orbit_pairs)
    print('Total bodies: ', len(orbit_tree))

    print('COM', end='')
    print_orbits(orbit_tree['COM'])
    total_orbits = sum([
        find_depth(orbit_tree, body) for body in orbit_tree.keys()])
    print('Total Orbits:', total_orbits)
    return total_orbits


def part2(filename):
    with open(filename) as f:
        orbit_pairs = [line.strip().split(')') for line in f]
    orbit_tree = process_orbits(orbit_pairs)
    print('Total bodies: ', len(orbit_tree))

    print('COM', end='')
    print_orbits(orbit_tree['COM'])
    your_body = orbit_tree['YOU'].parent.name
    santa_body = orbit_tree['SAN'].parent.name

    path = path_to_body(orbit_tree, your_body, santa_body)
    print('->'.join(path))
    return len(path) - 1


if __name__ == '__main__':
    print('Part 1:', part1(INPUT_FILE))
    print('Part 2:', part2(INPUT_FILE))

