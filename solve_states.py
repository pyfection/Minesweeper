def bomb_probability(state, x, y):
    max_probability = 0
    min_probability = 1

    if state[(x, y)] == -2:
        # If given field already flagged, should return 100% probability
        return 1

    for rx in range(-1, 2):
        for ry in range(-1, 2):
            nx, ny = x+rx, y+ry
            try:
                number_neighbor = state[(nx, ny)]
            except KeyError:
                continue
            if number_neighbor <= 0:
                # Is covered (-1), flagged (-2), to be uncovered (-3) or doesn't have any fields around it (shouldn't happen)
                continue

            flagged_count = 0
            neighbor_adjacent_covered = 0

            for rnx in range(-1, 2):
                for rny in range(-1, 2):
                    try:
                        neighbors_neighbor = state[(nx + rnx, ny + rny)]
                    except KeyError:
                        continue

                    if neighbors_neighbor == -1:
                        neighbor_adjacent_covered += 1
                    elif neighbors_neighbor == -2:
                        flagged_count += 1

            p = (number_neighbor - flagged_count) / neighbor_adjacent_covered

            if p > max_probability:
                max_probability = p
            elif p < min_probability:
                min_probability = p

    if min_probability == 0 and max_probability == 1:
        # Can't be guaranteed emtpy and bomb at the same time
        return None
    return max_probability if min_probability > 0. else min_probability


def possible_states(state: dict, edges: list, processed_edges=None):
    x, y = edges.pop(0)
    processed_edges = processed_edges or []
    solved_states = []  # List of lists of states (variable above)
    bomb_prob = bomb_probability(state, x, y)
    if bomb_prob is None:
        return solved_states

    if not edges:
        if bomb_prob > 0:  # If bomb is possible
            solved_states.append(processed_edges + [True])
        if bomb_prob < 1:  # If empty is possible
            solved_states.append(processed_edges + [False])
    else:
        if bomb_prob > 0:  # If bomb is possible
            new_state = state.copy()
            new_state[(x, y)] = -2
            states = possible_states(new_state, edges.copy(), processed_edges + [True])
            if states:
                solved_states.extend(states)
        if bomb_prob < 1:  # If empty is possible
            new_state = state.copy()
            new_state[(x, y)] = -3
            states = possible_states(new_state, edges.copy(), processed_edges + [False])
            if states:
                solved_states.extend(states)
    return solved_states


def state_probabilities(state: dict, edges: list):
    e = len(edges)
    states = possible_states(state, edges)
    n = len(states)
    prob = []
    for x in range(e):
        p = [states[y][x] for y in range(n)].count(True) / n
        prob.append(p)
    return prob


if __name__ == '__main__':
    board = [
        [-1, -1],
        [1, 1],
        [0, 0],
    ]
    state = {(x, y): v for y, row in enumerate(board) for x, v in enumerate(row)}
    edges = [(0, 0), (1, 0)]

    print(bomb_probability(state, 0, 0))

    print(possible_states(state, edges.copy()))

    print(state_probabilities(state, edges.copy()))
