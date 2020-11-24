import matplotlib.pyplot as plt

from knapsack import Knapsack
from hillclimbing.first import search as hc_first
from hillclimbing.best import search as hc_best
from evolution.population import Population

def main():
    knapsack = Knapsack("./ks_1000.dat")

    # Hill-climbing best improvement
    iterations = [(100, 64), (500, 32), (1_000, 16), (5_000, 8), (10_000, 4),(50_000, 2), (100_000, 1)]
    average_score = [0]
    average_evaluations = [0]
    for iters, repeats in iterations:
        print(f"Testing hill-climbing best improvement {repeats} time(s) with {iters} iterations.")
        total_score = 0
        total_eval = 0
        for repeat in range(repeats):
            score, evaluations = hc_best(knapsack, iters)
            total_score += score
            total_eval += evaluations
        average_score.append(total_score/repeats)
        average_evaluations.append(total_eval/repeats)

    plt.plot(average_evaluations, average_score, label="Hill-climbing best improvement")

    # Hill-climbing first improvement
    iterations = [(100, 64), (500, 32), (1_000, 16), (5_000, 8), (10_000, 4),(50_000, 2), (100_000, 1)]
    average_score = [0]
    average_evaluations = [0]
    for iters, repeats in iterations:
        print(f"Testing hill-climbing first improvement {repeats} time(s) with {iters} iterations.")
        total_score = 0
        total_eval = 0
        for repeat in range(repeats):
            score, evaluations = hc_first(knapsack, iters)
            total_score += score
            total_eval += evaluations
        average_score.append(total_score/repeats)
        average_evaluations.append(total_eval/repeats)

    plt.plot(average_evaluations, average_score, label="Hill-climbing first improvement")

    #print(score, evals)
    #score, evals = recuit_simule(knapsack)

    # Evolution
    iterations = [(100, 50), (500, 10), (1_000, 5), (5_000, 1), (10_000, 1)]
    average_score = [0]
    average_evaluations = [0]
    for iters, repeats in iterations:
        print(f"Testing evolution {repeats} time(s) with {iters} iterations.")
        total_score = 0
        total_eval = 0
        for repeat in range(repeats):
            pop = Population(10, knapsack)
            evaluations, score = pop.run(iters)
            total_score += score
            total_eval += evaluations
        average_score.append(total_score/repeats)
        average_evaluations.append(total_eval/repeats)

    plt.plot(average_evaluations, average_score, label="Evolution mu=10")

    plt.grid()
    plt.xlabel("Evaluations")
    plt.ylabel("Average performance")
    plt.figlegend()
    plt.show()

if __name__ == '__main__':
    main()
