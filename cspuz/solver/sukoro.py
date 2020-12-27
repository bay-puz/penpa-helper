# -*- coding: utf-8 -*-
import random
import math
import sys

from cspuz import Solver, graph, backend
from cspuz.constraints import count_true
from cspuz.puzzle import util


def solve_sukoro(height, width, problem):
    solver = Solver()

    has_number = solver.bool_array((height, width))
    graph.active_vertices_connected(solver, has_number)
    nums = solver.int_array((height, width), 0, 4)
    solver.add_answer_key(nums)
    solver.add_answer_key(has_number)

    for y in range(height):
        for x in range(width):
            neighbors = []
            if y > 0:
                neighbors.append(has_number[y-1, x])
                solver.ensure((has_number[y, x] & has_number[y-1, x]).then(nums[y, x] != nums[y-1, x]))
            if y < height - 1:
                neighbors.append(has_number[y+1, x])
                solver.ensure((has_number[y, x] & has_number[y+1, x]).then(nums[y, x] != nums[y+1, x]))
            if x > 0:
                neighbors.append(has_number[y, x-1])
                solver.ensure((has_number[y, x] & has_number[y, x-1]).then(nums[y, x] != nums[y, x-1]))
            if x < width - 1:
                neighbors.append(has_number[y, x+1])
                solver.ensure((has_number[y, x] & has_number[y, x+1]).then(nums[y, x] != nums[y, x+1]))
            solver.ensure(has_number[y, x].then(count_true(neighbors) == nums[y, x]))

    solver.ensure((~has_number).then(nums == 0))

    for y in range(height):
        for x in range(width):
            if problem[y][x] > 0:
                solver.ensure(nums[y, x] == problem[y][x])

    is_sat = solver.solve(backend.z3)

    return is_sat, nums, has_number


def compute_score(nums):
    score = 0
    for v in nums:
        if v.sol is not None:
            score += 1
    return score


def generate_sukoro(height, width, verbose=False):
    problem = [[0 for _ in range(width)] for _ in range(height)]
    score = 0
    temperature = 5.0
    fully_solved_score = height * width

    for step in range(height * width * 10):
        cand = []
        for y in range(height):
            for x in range(width):
                for n in range(1, 5):
                    if problem[y][x] != n:
                        cand.append((y, x, n))
        random.shuffle(cand)

        for y, x, n in cand:
            n_prev = problem[y][x]
            problem[y][x] = n

            sat, nums, has_number = solve_sukoro(height, width, problem)
            if not sat:
                score_next = -1
                update = False
            else:
                raw_score = compute_score(nums)
                if raw_score == fully_solved_score:
                    return problem
                clue_score = 0
                for y2 in range(height):
                    for x2 in range(width):
                        if problem[y2][x2] > 0:
                            clue_score += 3
                score_next = raw_score - clue_score
                update = (score < score_next or random.random() < math.exp((score_next - score) / temperature))

            if update:
                if verbose:
                    print('update: {} -> {}'.format(score, score_next), file=sys.stderr)
                score = score_next
                break
            else:
                problem[y][x] = n_prev

        temperature *= 0.995
    if verbose:
        print('failed', file=sys.stderr)
    return None


def _main():
    if len(sys.argv) == 1:
        # http://pzv.jp/p.html?sukoro/8/8/j3d1b2a4b33c2b2d3a13h1a2b1d1d1
        height = width = 8
        is_sat, nums, has_number = solve_sukoro(height, width, [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 1],
            [0, 0, 2, 0, 4, 0, 0, 3],
            [3, 0, 0, 0, 2, 0, 0, 2],
            [0, 0, 0, 0, 3, 0, 1, 3],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 2, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1],
        ])
        print('has_answer:', is_sat)
        if is_sat:
            ans = []
            for y in range(height):
                row = []
                for x in range(width):
                    if has_number[y, x].sol is not None:
                        if has_number[y, x].sol:
                            if nums[y, x].sol is not None:
                                row.append(str(nums[y, x].sol))
                            else:
                                row.append('o')
                        else:
                            row.append('x')
                    else:
                        row.append('?')
                ans.append(row)
            print(util.stringify_array(ans))
    else:
        height, width = map(int, sys.argv[1:])
        problem = generate_sukoro(height, width, True)
        print(util.stringify_array(problem, str))


if __name__ == '__main__':
    _main()
