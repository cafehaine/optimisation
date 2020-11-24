from random import shuffle
from typing import Tuple

from knapsack import Knapsack, random_solution


def search(knapsack: Knapsack, max_nb_eval: int) -> Tuple[float, int]:
    base_solution = random_solution(knapsack)
    base_score = knapsack.evaluate(base_solution)
    nb_eval = 1
    voisins_possibles = list(range(knapsack.items))

    while True:
        shuffle(voisins_possibles)
        current_score = base_score
        index_voisin = -1

        while (
            index_voisin + 1 < len(voisins_possibles)
            and current_score <= base_score
            and nb_eval <= max_nb_eval
        ):
            index_voisin += 1
            index = voisins_possibles[index_voisin]
            base_solution[index] = not base_solution[index]
            current_score = knapsack.evaluate(base_solution)
            nb_eval += 1
            base_solution[index] = not base_solution[index]

        if current_score > base_score:
            base_score = current_score
            index = voisins_possibles[index_voisin]
            base_solution[index] = not base_solution[index]
        elif index_voisin + 1 == len(voisins_possibles):
            break  # optimum local

        if nb_eval >= max_nb_eval:
            break

    return base_score, nb_eval
