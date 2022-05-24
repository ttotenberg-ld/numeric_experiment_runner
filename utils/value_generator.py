import matplotlib.pyplot as plt
import numpy as np
import random


'''
Returns a distribution of values given the following inputs:
CENTER: The mean of the distribution
SPREAD: The standard deviation or 'width' of the distribution. Remember that edge values may be up to ~3x above/below the standard deviation
ITERATIONS: The number of values that will be returned
'''
def normal_distribution(center, spread, iterations):
    value_array = np.random.default_rng().normal(center, spread, iterations)
    return value_array


def random_distribution(center, spread, iterations):
    low = int(center) - int(spread*3)
    high = int(center) + int(spread*3)
    value_array = []
    for i in range(iterations):
        value_array.append(random.randint(low, high))
    return value_array


def plot_histogram(data, variation):
    histogram = plt.hist(data, alpha=0.5, bins=100, label=str(variation))
    return histogram


'''
Example plot
'''
def example_plot():
    normal_example = normal_distribution(25, 5, 5000)
    another_normal_example = normal_distribution(30, 5, 5000)
    yet_another_normal_example = normal_distribution(40, 5, 5000)


    plot_histogram(normal_example, "variation1")
    plot_histogram(another_normal_example, "variation2")
    plot_histogram(yet_another_normal_example, "variation3")
    plt.legend(loc='upper right')

    plt.show()