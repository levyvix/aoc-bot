from __future__ import annotations

import itertools
from collections import Counter

MIN_OVERLAP = 12


def _parse(data: str) -> list[list[tuple[int, int, int]]]:
    scanners: list[list[tuple[int, int, int]]] = []
    for block in data.strip().split("\n\n"):
        beacons: list[tuple[int, int, int]] = []
        for line in block.strip().splitlines()[1:]:
            if not line.strip():
                continue
            x, y, z = map(int, line.split(","))
            beacons.append((x, y, z))
        if beacons:
            scanners.append(beacons)
    return scanners


def _rotation_functions() -> list:
    rotations: list = []
    for axes in itertools.permutations((0, 1, 2)):
        for signs in itertools.product((-1, 1), repeat=3):
            matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            for row, axis in enumerate(axes):
                matrix[row][axis] = signs[row]
            det = (
                matrix[0][0]
                * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
                - matrix[0][1]
                * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
                + matrix[0][2]
                * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
            )
            if det != 1:
                continue

            def make_rot(m: list[list[int]] = matrix):
                def rot_fn(p: tuple[int, int, int]) -> tuple[int, int, int]:
                    return (
                        m[0][0] * p[0] + m[0][1] * p[1] + m[0][2] * p[2],
                        m[1][0] * p[0] + m[1][1] * p[1] + m[1][2] * p[2],
                        m[2][0] * p[0] + m[2][1] * p[1] + m[2][2] * p[2],
                    )

                return rot_fn

            rotations.append(make_rot())
    return rotations


def _find_alignment(
    known: set[tuple[int, int, int]],
    candidate: list[tuple[int, int, int]],
    rotations: list,
) -> tuple[tuple[int, int, int], list[tuple[int, int, int]]] | None:
    for rot_fn in rotations:
        rotated = tuple(rot_fn(b) for b in candidate)
        offset_counts: Counter[tuple[int, int, int]] = Counter()
        for rb in rotated:
            for known_pt in known:
                offset = (
                    known_pt[0] - rb[0],
                    known_pt[1] - rb[1],
                    known_pt[2] - rb[2],
                )
                offset_counts[offset] += 1
        for offset, count in offset_counts.items():
            if count < MIN_OVERLAP:
                continue
            transformed = {
                (pt[0] + offset[0], pt[1] + offset[1], pt[2] + offset[2])
                for pt in rotated
            }
            if len(transformed & known) >= MIN_OVERLAP:
                return offset, list(transformed)
    return None


def _assemble(
    scanners: list[list[tuple[int, int, int]]],
) -> tuple[set[tuple[int, int, int]], dict[int, tuple[int, int, int]]]:
    rotations = _rotation_functions()
    aligned: set[tuple[int, int, int]] = set(scanners[0])
    scanner_positions: dict[int, tuple[int, int, int]] = {0: (0, 0, 0)}
    scanner_beacons: dict[int, set[tuple[int, int, int]]] = {0: set(scanners[0])}
    pending = set(range(1, len(scanners)))

    while pending:
        progress = False
        for idx in sorted(pending):
            for ref_idx in scanner_beacons:
                result = _find_alignment(
                    scanner_beacons[ref_idx], scanners[idx], rotations
                )
                if result is not None:
                    scanner_pos, new_beacons = result
                    aligned.update(new_beacons)
                    scanner_positions[idx] = scanner_pos
                    scanner_beacons[idx] = set(new_beacons)
                    pending.remove(idx)
                    progress = True
                    break
            if progress:
                break
        if not progress:
            raise RuntimeError("could not align all scanners")
    return aligned, scanner_positions


def solve(data: str) -> str:
    scanners = _parse(data)
    beacons, _ = _assemble(scanners)
    return str(len(beacons))
