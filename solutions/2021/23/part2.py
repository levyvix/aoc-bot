from __future__ import annotations

import heapq

ENERGY = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOM_DEPTH = 4
GOAL = tuple(c * ROOM_DEPTH for c in "ABCD")
DOORS = (2, 4, 6, 8)
ROOM_COLS = (3, 5, 7, 9)
INSERTED_LINES = ("  #D#C#B#A#", "  #D#B#A#C#")


def _expand_input(data: str) -> list[str]:
    lines = data.strip().splitlines()
    return [lines[0], lines[1], lines[2], *INSERTED_LINES, lines[3], lines[4]]


def _parse(data: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    lines = _expand_input(data)
    room_lines = lines[2:6]
    rooms = tuple(
        "".join(room_lines[row][col] for row in range(ROOM_DEPTH))
        for col in ROOM_COLS
    )
    hallway = tuple("." * 11)
    return rooms, hallway


def _top_pod(room: str) -> tuple[int, str] | None:
    for depth, pod in enumerate(room):
        if pod != ".":
            return depth, pod
    return None


def _can_enter(rooms: tuple[str, ...], room_idx: int, pod: str) -> bool:
    target = "ABCD"[room_idx]
    if pod != target:
        return False
    return all(c == "." or c == target for c in rooms[room_idx])


def _hallway_path_clear(hallway: tuple[str, ...], pos: int, door: int) -> bool:
    if pos < door:
        for i in range(pos + 1, door):
            if hallway[i] != ".":
                return False
    elif pos > door:
        for i in range(door + 1, pos):
            if hallway[i] != ".":
                return False
    return True


def _moves(
    rooms: tuple[str, ...], hallway: tuple[str, ...]
) -> list[tuple[int, tuple[str, ...], tuple[str, ...]]]:
    moves: list[tuple[int, tuple[str, ...], tuple[str, ...]]] = []

    for room_idx, room in enumerate(rooms):
        top = _top_pod(room)
        if top is None:
            continue
        depth, pod = top
        door = DOORS[room_idx]
        cost_per = ENERGY[pod]
        exit_steps = depth + 1

        for pos in range(door - 1, -1, -1):
            if pos in DOORS:
                continue
            if hallway[pos] != ".":
                break
            new_hall = list(hallway)
            new_hall[pos] = pod
            new_room = list(room)
            new_room[depth] = "."
            new_rooms = list(rooms)
            new_rooms[room_idx] = "".join(new_room)
            moves.append(
                (
                    cost_per * (exit_steps + door - pos),
                    tuple(new_rooms),
                    tuple(new_hall),
                )
            )

        for pos in range(door + 1, 11):
            if pos in DOORS:
                continue
            if hallway[pos] != ".":
                break
            new_hall = list(hallway)
            new_hall[pos] = pod
            new_room = list(room)
            new_room[depth] = "."
            new_rooms = list(rooms)
            new_rooms[room_idx] = "".join(new_room)
            moves.append(
                (
                    cost_per * (exit_steps + pos - door),
                    tuple(new_rooms),
                    tuple(new_hall),
                )
            )

    for pos, pod in enumerate(hallway):
        if pod == ".":
            continue
        for room_idx in range(4):
            door = DOORS[room_idx]
            if not _hallway_path_clear(hallway, pos, door):
                continue
            if not _can_enter(rooms, room_idx, pod):
                continue
            room = rooms[room_idx]
            depth = next((i for i, c in enumerate(room) if c == "."), None)
            if depth is None:
                continue
            enter_steps = abs(pos - door) + depth + 1
            new_hall = list(hallway)
            new_hall[pos] = "."
            new_room = list(room)
            new_room[depth] = pod
            new_rooms = list(rooms)
            new_rooms[room_idx] = "".join(new_room)
            moves.append(
                (
                    ENERGY[pod] * enter_steps,
                    tuple(new_rooms),
                    tuple(new_hall),
                )
            )

    return moves


def _solve_state(rooms: tuple[str, ...], hallway: tuple[str, ...]) -> int:
    start = (rooms, hallway)
    pq: list[tuple[int, tuple[str, ...], tuple[str, ...]]] = [(0, rooms, hallway)]
    best: dict[tuple[tuple[str, ...], tuple[str, ...]], int] = {start: 0}

    while pq:
        cost, rooms, hallway = heapq.heappop(pq)
        state = (rooms, hallway)
        if cost > best.get(state, float("inf")):
            continue
        if rooms == GOAL and all(c == "." for c in hallway):
            return cost
        for step_cost, new_rooms, new_hall in _moves(rooms, hallway):
            new_state = (new_rooms, new_hall)
            total = cost + step_cost
            if total < best.get(new_state, float("inf")):
                best[new_state] = total
                heapq.heappush(pq, (total, new_rooms, new_hall))

    raise RuntimeError("no solution found")


def solve(data: str) -> str:
    rooms, hallway = _parse(data)
    return str(_solve_state(rooms, hallway))
