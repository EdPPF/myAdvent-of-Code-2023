def _read_file(path: str) -> list[str]:
    file = open(path, 'r')
    return list(
            filter(
                lambda x: x != '\n',
                file.readlines())
        )


def _remove_newline(line: str):
    line = line.translate(str.maketrans('', '', '\n'))
    return line

def _remove_newline_from_list(lines: list[str]):
    for line_idx in range(len(lines)):
        lines[line_idx] = _remove_newline(lines[line_idx])


def _create_range(line: str):
    chars = line.split(' ')
    numbers = list(map(int, chars))
    dst_start = numbers[0]
    src_start = numbers[1]
    length    = numbers[2]
    dst_range = list(range(dst_start, dst_start+length, 1))
    src_range = list(range(src_start, src_start+length, 1))
    return dict(zip(src_range, dst_range))

def _compose_maps(lines: list[str]):
    maps = {}
    current = ''
    for line in lines:
        if 'map' in line:
            current = line
            maps[current] = {}
            continue
        maps[current] |= _create_range(line) # nice
    return maps


#############################Part 1##############################
def first_impact(path:str):
    lines = _read_file(path)
    _remove_newline_from_list(lines)

    seeds = lines[0].split(' ')[1:]
    lines = lines[1:]
    all_maps = _compose_maps(lines)

    corresps = []
    for seed in seeds:
        current_src = int(seed)
        current_corresp = []
        current_corresp.append(current_src)
        for maps in all_maps.values():
            if current_src in maps.keys():
                current_src = maps[current_src]
                current_corresp.append(current_src)
            else:
                current_corresp.append(current_src)
        corresps.append(current_corresp)

    return min([corr[-1] for corr in corresps])

#############################Part 2##############################
def second_impact(path: str):
    return

print(first_impact("./input.txt"))
