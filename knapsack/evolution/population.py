import random
from typing import NamedTuple, Tuple

from knapsack import Knapsack, Solution, random_solution

class Individu(NamedTuple):
    solution: Solution
    score: float

class Population:
    def __init__(self, mu: int, knapsack: Knapsack):
        self.knapsack = knapsack
        parents = [random_solution(knapsack) for i in range(mu)]
        self._population = [Individu(parent, knapsack.evaluate(parent)) for parent in parents]
        self.mu = mu

    @staticmethod
    def children(parent_a: Solution, parent_b: Solution) -> Tuple[Solution, Solution]:
        """Return two children from the given parents."""
        pivot = random.randint(1, len(parent_a) - 1)
        child_a = parent_a[:pivot] + parent_b[pivot:]
        Population.mutate(child_a)
        child_b = parent_b[:pivot] + parent_a[pivot:]
        Population.mutate(child_b)
        return child_a, child_b

    @staticmethod
    def mutate(solution):
        """Random mutation of a solution."""
        for index, value in enumerate(solution):
            if random.random() <= 1 / len(solution):
                solution[index] = not value

    def run(self, iters: int) -> Tuple[Solution, float]:
        self._population.sort(key=lambda individu: individu.score, reverse=True)
        for i in range(iters):
            for j in range(self.mu//2): # generate mu/2 couples, for a total 2*mu population after reinsertion
                parent_a = random.choice(self._population).solution
                parent_b = random.choice(self._population).solution
                child_a, child_b = Population.children(parent_a, parent_b)
                self._population.append(Individu(child_a, self.knapsack.evaluate(child_a)))
                self._population.append(Individu(child_b, self.knapsack.evaluate(child_b)))
            # Selection
            self._population.sort(key=lambda individu: individu.score, reverse=True)
            self._population = self._population[:self.mu]

        return self._population[0]

