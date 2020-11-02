from random import getrandbits
from typing import Collection, List

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


def hill_climber_best_improvement(knapsack: Knapsack) -> Solution:
    """Use the hill climber best improvement to find a solution."""
    base_solution = random_solution(knapsack)

    while True:
        neighbours = get_neighbours(base_solution)
        best = max(neighbours, key=lambda sol: sol.score)
        if best.score > base_solution.score:
            base_solution = best
        else:
            break # Optimum local

    return base_solution


def main():
    knapsack = Knapsack("./ks_1000.dat")

    solution_climber = hill_climber_best_improvement(knapsack)
    print(solution_climber.score)


if __name__ == '__main__':
    main()
