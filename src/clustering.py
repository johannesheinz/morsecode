import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

from decoder import Signal


class Clustering:
    """
    A machine learning algorithm that uses unsupervised learning processes in order to determine clusters.
    """
    _kmeans: KMeans
    _prediction: list
    _n_clusters: int = 0

    def __init__(self, number_of_clusters: int):
        """
        Configures the algorithm
        :param number_of_clusters: The number of clusters for the algorithm to form.
        """
        self._n_clusters = number_of_clusters

    def train(self, batch: list) -> list:
        """
        Forms the configured number of clusters out of the given batch.
        :param batch: Training data in the form of a list of tuples.
        :return: Returns a list of labels for each data point
        """

        data = np.array(batch)
        n_samples = len(batch)
        print("Samples: %d" % n_samples)

        self._kmeans = KMeans(n_clusters=self._n_clusters, init='k-means++', random_state=150).fit(data)
        self._prediction = self._kmeans.predict(data)

        plt.figure(figsize=(12, 12))
        plt.scatter(data[:, 0], data[:, 1], c=self._prediction)
        plt.title("k-means++")

        plt.show()
        return self._prediction

    def get_label_mapping(self) -> dict:
        """
        Matches the internal labels to pre-defined enums that contain semantics.
        :return: A mapping that contains a Signal for every internally used label.
        """
        mapping = dict()
        print()

        model_long = ((0.30, 0.85), (0.39, 0.93), (0.25, 0.99))
        self._map(mapping, model_long, Signal.LONG)

        model_short = ((0.10, 0.85), (0.15, 0.92), (0.08, 0.99))
        self._map(mapping, model_short, Signal.SHORT)

        model_pause_short = ((0.10, 0.05), (0.15, 0.15), (0.08, 0.10))
        self._map(mapping, model_pause_short, Signal.PAUSE_SHORT)

        model_pause_medium = ((0.30, 0.05), (0.39, 0.15), (0.25, 0.10))
        self._map(mapping, model_pause_medium, Signal.PAUSE_MEDIUM)

        model_pause_long = ((1.70, 0.05), (2.81, 0.15), (1.65, 0.10))
        self._map(mapping, model_pause_long, Signal.PAUSE_LONG)

        # TODO : Plot test points

        print()
        return mapping

    def _map(self, _map: dict, tuples: list, signal: Signal) -> None:
        prediction = self._kmeans.predict(np.array(tuples))

        _sum = 0.0
        for label in prediction:
            _sum += label
        print("%20s -> %f" % (signal, (_sum / len(prediction))))

        label = round(_sum / len(prediction))
        _map[label] = signal
