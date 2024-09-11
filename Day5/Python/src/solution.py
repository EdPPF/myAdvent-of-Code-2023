def _open_file(path: str) -> list[str]:
    with open(file=path) as arc:
        lines = arc.read().split('\n')
    return lines[:-1]


def _compose_maps(lines: list[str]) -> list[list[str | list[int]]]:
    maps = []
    current_map = []
    lines_len = len(lines)
    counter = 0
    for line in lines:
        counter += 1
        if line == '':
            maps.append(current_map)
            current_map = []
            continue
        if 'map' in line:
            current_map.append(line)
            continue
        numbers = line.split(' ')
        current_map.append(list(map(int, numbers)))
        if counter >= lines_len:
            maps.append(current_map)
    return maps


#############################Part 1##############################
def first_impact(path:str):
    lines = _open_file(path)

    seeds = [line for line in lines[0].split(' ') if line.isdecimal()]

    lines = lines[2:]
    # print(lines)
    maps = _compose_maps(lines)
    # print(maps)
    corresps = []
    for seed in seeds:
        current_corresp = []
        src = int(seed)
        current_corresp.append(src)
        # print(f"On seed {seed}:")
        for map in maps:
            # print(f"{' '*4}Current src: {src}")
            map_len = len(map)
            # print(f"{' '*4}Current map (len={map_len}): {map}")
            counter = 0
            for rang in map[1:]:
                counter += 1
                src_start = rang[0]
                dst_start = rang[1]
                length    = rang[2]
                # print(f"{' '*4}src_start: {src_start}\n{' '*4}dst_start: {dst_start}\n{' '*4}length: {length}")

                src_range = list(range(src_start, src_start+length, 1))
                dst_range = list(range(dst_start, dst_start+length, 1))
                # print(f"{' '*4}SRC_RANGE: {src_range}")
                # print(f"{' '*4}DST_RANGE: {dst_range}")
                if src in dst_range:
                    corresp_idx = dst_range.index(src)
                    src = src_range[corresp_idx]
                    # print(f"{' '*8}src NOW: {src}")
                    current_corresp.append(src)
                    # Break on first match:
                    break
                else:
                    # print(f"{' '*8} Counter: {counter}")
                    if counter >= map_len-1:
                        # print(f"{' '*8}src NOW: {src}")
                        current_corresp.append(src)
            # print(f"->> List Now: {current_corresp}")
        corresps.append(current_corresp)
        # print(f"-> {current_corresp}")

    return min([corr[-1] for corr in corresps])

#############################Part 2##############################
def second_impact(path: str):
    return

print(first_impact("./input.txt"))
