from matplotlib.pyplot import figure, bar, show

from .types import NGramFrequencyMap


def plot_frequency(n_gram_frequencies: NGramFrequencyMap, **kwargs) -> None:
    """
    :param n_gram_frequencies: NGramFrequencyMap - map containing frequencies for given n-gram
    :key bar_values: Boolean - controls visibility of value depicted by bar on the top of it
    """
    fig = figure()
    ax = fig.add_subplot(111)

    values = list(n_gram_frequencies.values())
    keys = list(n_gram_frequencies.keys())
    bar(keys, values)

    if kwargs.get('bar_values', False):
        for index, value in enumerate(values):
            ax.text(index, value * 1.01, '{:.5f}'.format(value), ha='center')
    show()

