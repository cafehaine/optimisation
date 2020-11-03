import math
from random import getrandbits, randrange, shuffle
from typing import Collection, List, Tuple

class Knapsack:
    """A container for the required data to describe a knapsack situation."""
    def __init__(self, path: str):
        with open(path, "r") as data:
            self.items = int(data.readline())
            self.profits = [int(elm) for elm in data.readline().split()]
            self.weights = [int(elm) for elm in data.readline().split()]
            self.max_weight = int(data.readline())

        self.beta = max([profit/weight for (profit, weight) in zip(self.profits, self.weights)])


    def evaluate(self, solution: List[bool]) -> float:
        """Compute the score for a solution."""
        weight = 0
        profit = 0
        for index, include in enumerate(solution):
            if include:
                weight += self.weights[index]
                profit += self.profits[index]
        if weight >= self.max_weight:
            profit -= self.beta * (weight - self.max_weight)

        return profit


def random_solution(knapsack: Knapsack) -> List[bool]:
    """Return a random solution for a given knapsack."""
    return [bool(getrandbits(1)) for i in range(len(knapsack.weights))]


def hill_climber_best_improvement(knapsack: Knapsack) -> Tuple[float, int]:
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

        if best_score > base_score:
            base_solution[index_solution] = not base_solution[index_solution]
            base_score = best_score
        else:
            break # Optimum local

    return base_score, nb_eval


def hill_climber_first_improvement(knapsack: Knapsack, max_nb_eval: int) -> Tuple[float, int]:
    base_solution = random_solution(knapsack)
    base_score = knapsack.evaluate(base_solution)
    nb_eval = 1
    voisins_possibles = [i for i in range(knapsack.items)]

    while True:
        shuffle(voisins_possibles)
        current_score = base_score
        index_voisin = -1

        while index_voisin + 1 < len(voisins_possibles) and current_score <= base_score and nb_eval <= max_nb_eval:
            index_voisin += 1
            index = voisins_possibles[index_voisin]
            base_solution[index] = not base_solution[index]
            current_score = knapsack.evaluate(base_solution)
            nb_eval += 1
            base_solution[index] = not base_solution[index]

        if current_score > base_score:
            print(f"Found a better solution: {current_score} > {base_score}")
            base_score = current_score
            index = voisins_possibles[index_voisin]
            base_solution[index] = not base_solution[index]
        elif index_voisin +1 == len(voisins_possibles):
            print("Out of neighbours")
            break # optimum local

        if nb_eval >= max_nb_eval:
            break

    return base_score, nb_eval


def main():
    knapsack = Knapsack("./ks_1000.dat")

    #score, evals = hill_climber_best_improvement(knapsack)
    #print(score, evals)
    score, evals = hill_climber_first_improvement(knapsack, 200_000)
    print(score, evals)


if __name__ == '__main__':
    main()
