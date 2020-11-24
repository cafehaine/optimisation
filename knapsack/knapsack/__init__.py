import math
from random import getrandbits, randrange, shuffle, random
from typing import Collection, List, Tuple

Solution = List[bool]

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


def hill_climber_best_improvement(knapsack: Knapsack, max_evals: int) -> Tuple[float, int]:
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
            base_score = current_score
            index = voisins_possibles[index_voisin]
            base_solution[index] = not base_solution[index]
        elif index_voisin +1 == len(voisins_possibles):
            break # optimum local

        if nb_eval >= max_nb_eval:
            break

    return base_score, nb_eval


def initial_temp(knapsack, n=None, tau_zero=0.35) -> float:
    if n is None:
        n = knapsack.items // 10

    sum_delta = 0

    for _ in range(n):
        s = random_solution(knapsack)
        score_s = knapsack.evaluate(s)
        index = randrange(knapsack.items)
        s[index] = not s[index]
        score_sprime = knapsack.evaluate(s)
        sum_delta += score_sprime - score_s

    avg_delta = sum_delta / n

    # ln(tau_zero) = avg_delta / T_zero
    # T_zero = avg_delta / ln(tau_zero)

    return avg_delta / math.log(tau_zero)


def recuit_simule(knapsack) -> Tuple[float, int]:
    s = random_solution(knapsack)
    score_s = knapsack.evaluate(s)
    nb_eval = 1
    # T = initial_temp(knapsack)
    T = 50
    alpha = 0.9

    n_sans_accept = 0
    n_tentees = 0
    n_acceptees = 0
    while True:
        index = randrange(knapsack.items)
        s[index] = not s[index]
        score_sprime = knapsack.evaluate(s)
        nb_eval += 1
        delta = score_sprime - score_s

        keep = False

        if delta>0:
            keep = True
        else:
            u = random()
            if u < math.exp(delta/T):
                keep = True

        n_tentees +=1

        if keep:
            score_s = score_sprime
            n_sans_accept = 0
            n_acceptees += 1
        else:
            s[index] = not s[index]
            n_sans_accept += 1

        if n_tentees == 100:
            n_tentees = 0
            T *= alpha
        if n_acceptees == 12:
            n_acceptees = 0
            T *= alpha

        if n_sans_accept == 30:
            break

    return score_s, nb_eval


def perturbation(s: List[bool], k: int):
    for _ in range(k):
        i = randrange(len(s))
        s[i] = not s[i]


def iterated_local_search(knapsack) -> Tuple[float, int]:
    """
    s = random_solution(knapsack)
    score_s = knapsack.evaluate(s)
    nb_eval = 1
    s←localSearch(s)
    while True:
        s′←perturbation(s)
        s′←localSearch(s′)
        Si accept(s,s′) Alors
            s←s′
        if Critère d’arrêt vérifié:
            break
    return score_s, nb_eval
    """
