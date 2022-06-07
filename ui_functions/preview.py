import matplotlib.pyplot as plt
import numpy as np
import random
from ui_functions.variations import get_current_variations, get_specific_value
    

'''
Returns a distribution of values given the following inputs:
CENTER: The mean of the distribution
SPREAD: The standard deviation or 'width' of the distribution. Edge values may be up to ~3x above/below the standard deviation
EVENTS: The number of values that will be returned
'''
def normal_distribution(center, spread, events):
    value_array = np.random.default_rng().normal(center, spread, events)
    return value_array

# Currently not implemented, could implement for alternate distributions later
def random_distribution(center, spread, events):
    low = int(center) - int(spread*3)
    high = int(center) + int(spread*3)
    value_array = []
    for i in range(events):
        value_array.append(random.randint(low, high))
    return value_array


def plot_histogram(data, variation):
    histogram = plt.hist(data, alpha=0.5, bins=100, label=str(variation))
    return histogram

    

'''
Action called when the preview button is clicked
'''
def preview_clicked(self):
    self.figure.clear()

    events = str(self.events.text())
    variations = get_current_variations(self)

    for i in range(len(variations)):
        center_number = int(get_specific_value(self, str(variations[i]), 'center'))
        spread_number = int(get_specific_value(self, str(variations[i]), 'spread'))
        distribution = normal_distribution(center_number, spread_number, int(events))
        plot_histogram(distribution, variations[i])

    plt.legend(loc='upper right')

    # refresh canvas
    self.canvas.draw()