from knapsack import Knapsack, hill_climber_best_improvement
from evolution.population import Population

def main():
    knapsack = Knapsack("./ks_1000.dat")

    score, evals = hill_climber_best_improvement(knapsack)
    print(score, evals)
    #score, evals = hill_climber_first_improvement(knapsack, 200_000)
    #print(score, evals)
    #score, evals = recuit_simule(knapsack)
    pop = Population(10, knapsack)
    solution, score = pop.run(1_000)
    print(score)


if __name__ == '__main__':
    main()
