import math
from typing import Tuple

from knapsack import Knapsack, random_solution


def search(knapsack: Knapsack, max_evals: int) -> Tuple[float, int]:
    """Use the hill climber best improvement to find a solution."""
    base_solution = random_solution(knapsack)
    base_score = knapsack.evaluate(base_solution)
    nb_eval = 1

    while True:
        best_score = -math.inf
        index_solution = -1

        for i in range(knapsack.items):
            base_solution[i] = not base_solution[i]
            score = knapsack.evaluate(base_solution)
            nb_eval += 1

            if score > best_score:
                best_score = score
                index_solution = i

            base_solution[i] = not base_solution[i]

        if nb_eval >= max_evals:
            break

        if best_score > base_score:
            base_solution[index_solution] = not base_solution[index_solution]
            base_score = best_score
        else:
            break  # Optimum local

    return base_score, nb_eval
