import matplotlib.pyplot as plt
import numpy as np


def plot(stats_vec, size, pop):
    txt = ""
    for i, stats in enumerate(stats_vec):
        best_fitness = np.array(stats[0])
        worst_fitness = np.array(stats[1])
        avg_fitness = np.array(stats[2])
        x = [i for i in range(1, len(best_fitness) + 1)]
        plt.plot(x[5:], best_fitness[5:], color='green')
        plt.plot(x[5:], worst_fitness[5:], color='red')
        plt.plot(x[5:], avg_fitness[5:], color='blue')
        txt = txt + f"run {i}: best fitness = {best_fitness[-1]} after {len(best_fitness)} generations.\n"

    plt.title(f"Puzzle of size {size}x{size} with Population {pop}")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(
        handles=[plt.Line2D([], [], color='green'), plt.Line2D([], [], color='red'), plt.Line2D([], [], color='blue')],
        labels=['Best Fitness', 'Worst Fitness', 'Average Fitness'])
    plt.text(0.2, 0.6, txt, fontsize=10, transform=plt.gca().transAxes)
    plt.show()
