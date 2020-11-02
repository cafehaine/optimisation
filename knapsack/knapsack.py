from random import getrandbits, randrange, shuffle
from typing import Collection, List, Tuple

class Knapsack:
    """A container for the required data to describe a knapsack situation."""
    def __init__(self, path: str):
        with open(path, "r") as data:
            items = int(data.readline())
            self.profits = [int(elm) for elm in data.readline().split()]
            self.weights = [int(elm) for elm in data.readline().split()]
            self.max_weight = int(data.readline())

        self.beta = max([profit/weight for (profit, weight) in zip(self.profits, self.weights)])


class Solution:
    """A boolean mask to describe a knapsack solution."""
    def __init__(self, knapsack: Knapsack, mask: List[bool]):
        self.mask = mask
        self.knapsack = knapsack
        self.score = self._eval()

    def _eval(self) -> float:
        weight = 0
        profit = 0
        for index, include in enumerate(self.mask):
            if include:
                weight += self.knapsack.weights[index]
                profit += self.knapsack.profits[index]
        if weight >= self.knapsack.max_weight:
            profit -= self.knapsack.beta * (weight - self.knapsack.max_weight)

        return profit


def random_solution(knapsack: Knapsack) -> Solution:
    """Return a random solution for a given knapsack."""
    mask = [getrandbits(1) for i in range(len(knapsack.weights))]
    return Solution(knapsack, mask)


def get_neighbours(base_solution) -> Collection[Solution]:
    """Return all the neighbours for a given solution."""
    output = []
    for i in range(len(base_solution.mask)):
        new_mask = base_solution.mask.copy()
        new_mask[i] = not new_mask[i]
        output.append(Solution(base_solution.knapsack, new_mask))
    return output


def get_random_neighbour(base_solution) -> Solution:
    mask = base_solution.mask.copy()
    index = randrange(len(mask))
    mask[index] = not mask[index]

    return Solution(base_solution.knapsack, mask)


def hill_climber_best_improvement(knapsack: Knapsack) -> Tuple[Solution, int]:
    """Use the hill climber best improvement to find a solution."""
    base_solution = random_solution(knapsack)
    nb_eval = 1

    while True:
        neighbours = get_neighbours(base_solution)
        nb_eval += len(neighbours)
        best = max(neighbours, key=lambda sol: sol.score)
        if best.score > base_solution.score:
            base_solution = best
        else:
            break # Optimum local

    return base_solution, nb_eval


def get_neighbour(solution: Solution, index: int) -> Solution:
    mask = solution.mask.copy()
    mask[index] = not mask[index]
    return Solution(solution.knapsack, mask)


def hill_climber_first_improvement(knapsack: Knapsack, max_nb_eval: int) -> Solution:
    solution = random_solution(knapsack)
    nb_eval = 1
    voisins_possibles = [i for i in range(len(solution.mask))]

    while True:
        print(solution.score, nb_eval)
        shuffle(voisins_possibles)

        index_voisin = 0

        x_prime = get_neighbour(solution, voisins_possibles[index_voisin])
        nb_eval += 1
        index_voisin += 1

        while index_voisin < len(voisins_possibles) and solution.score > x_prime.score and nb_eval <= max_nb_eval:
            x_prime = get_neighbour(solution, voisins_possibles[index_voisin])
            nb_eval += 1
            index_voisin += 1

        if solution.score < x_prime.score:
            print(f"Found better score: {solution.score} < {x_prime.score}")
            solution = x_prime
        elif index_voisin == len(voisins_possibles):
            print("Out of neighbours")
            break # optimum local

        if nb_eval >= max_nb_eval:
            break
    print(solution.score, nb_eval)

    return solution, nb_eval


def main():
    knapsack = Knapsack("./ks_1000.dat")

    #solution_climber, evals = hill_climber_best_improvement(knapsack)
    #print(solution_climber.score, evals)
    solution_climber, evals = hill_climber_first_improvement(knapsack, 200_000)
    print(solution_climber.score, evals)


if __name__ == '__main__':
    main()
