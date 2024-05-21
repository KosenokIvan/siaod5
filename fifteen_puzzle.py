from typing import List, Tuple
from queue import PriorityQueue


def check_if_solvable(state: Tuple[int, ...]):
    inv_count = 0
    for i in range(len(state) - 1):
        if state[i] == 0:
            continue
        for j in range(i + 1, len(state)):
            if state[j] == 0:
                continue
            if state[j] < state[i]:
                inv_count += 1
    size = int(len(state) ** .5)
    if size % 2 == 0:
        empty_cell_row = size - (state.index(0) // size)
        return inv_count % 2 != empty_cell_row % 2
    return inv_count % 2 == 0


def check_if_solved(state: Tuple[int, ...]):
    return state[-1] == 0 and all(map(lambda i: state[i] < state[i + 1], range(len(state) - 2)))


def heuristic(state):
    linear_conflict = 0
    size = int(len(state) ** .5)
    for i in range(len(state)):
        if state[i] != i + 1 and state[i] != 0:
            goal_row = (state[i] - 1) // size
            goal_col = (state[i] - 1) % size
            cur_row = i // size
            cur_col = i % size

            if goal_row == cur_row:
                for j in range(i + 1, (cur_row + 1) * size):
                    if not 0 <= j < len(state):
                        continue
                    if state[j] != j + 1 and state[j] != 0 and (state[j] - 1) // size == cur_row:
                        linear_conflict += 1
            if goal_col == cur_col:
                for j in range(i + size, (cur_col + 1)*size + cur_row*size, size):
                    if not 0 <= j < len(state):
                        continue
                    if state[j] != j + 1 and state[j] != 0 and (state[j] - 1) % size == cur_col:
                        linear_conflict += 1
    return heuristic_manhattan(state) + linear_conflict


def heuristic_manhattan(state):
    distance = 0
    size = int(len(state) ** .5)
    for i in range(len(state)):
        if state[i] != i + 1 and state[i] != 0:
            goal_row = (state[i] - 1) // size
            goal_col = (state[i] - 1) % size
            current_row = i // size
            current_col = i % size
            distance += abs(goal_row - current_row) + abs(goal_col - current_col)
    return distance


def generate_states(state: Tuple[int, ...]):
    zero_index = state.index(0)
    new_states = []
    size = int(len(state) ** .5)
    for move in [-size, size, -1, 1]:
        new_index = zero_index + move
        if (0 <= new_index < len(state)
                and (zero_index % size != 0 or new_index % size != size - 1)
                and (zero_index % size != size - 1 or new_index % size != 0)):
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            new_states.append((tuple(new_state), new_state[zero_index]))
    return new_states


def solve(state: Tuple[int, ...]):
    frontier = PriorityQueue()
    frontier.put((0, state))
    prev_state = {state: (None, None)}
    min_heuristic = 1000000000
    while frontier.not_empty:
        cur_cost, cur_state = frontier.get()
        if check_if_solved(cur_state):
            path = []
            while cur_state is not None:
                cur_state, moved_num = prev_state[cur_state]
                if moved_num is not None:
                    path.append(moved_num)
            return path[::-1]
        for next_state, moved_num in generate_states(cur_state):
            if next_state not in prev_state:
                next_heuristic = heuristic(next_state)
                if next_heuristic < min_heuristic:
                    min_heuristic = next_heuristic
                    # print(f"DEBUG: {min_heuristic}")
                priority = cur_cost + next_heuristic + 1
                frontier.put((priority, next_state))
                prev_state[next_state] = cur_state, moved_num
    return []


if __name__ == '__main__':
    positions = [
        # (8, 4, 12, 3, 14, 0, 9, 15, 7, 2, 5, 1, 10, 11, 13, 6),
        # (12, 1, 2, 15, 11, 6, 5, 8, 7, 10, 9, 4, 0, 13, 14, 3),
        # (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, 0),
        # (3, 4, 7, 2, 9, 1, 6, 15, 5, 14, 10, 12, 13, 11, 8, 0),
        # (0, 4, 3, 7, 5, 10, 14, 15, 1, 8, 2, 11, 12, 6, 9, 13),
        # (5, 1, 2, 3, 9, 7, 10, 4, 14, 13, 6, 11, 15, 12, 8, 0)
        (4, 3, 6, 1, 8, 0, 2, 5, 7),
        (1, 2, 7, 3, 4, 6, 0, 8, 5),
        (1, 4, 2, 0, 3, 6, 8, 5, 7),
        (3, 8, 4, 6, 7, 0, 1, 2, 5),
        (1, 2, 3, 7, 0, 4, 8, 6, 5),
        (5, 2, 7, 8, 4, 0, 1, 3, 6)
    ]
    for pos in positions:
        print(pos)
        if check_if_solvable(pos):
            solution = solve(pos)
            if solution:
                for i, num in enumerate(solution, 1):
                    print(f"\tStep {i}: Move {num}")
            else:
                print("No solution!")
        else:
            print("No solution!")
        print("=" * 45)
