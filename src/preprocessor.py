import csv
import math

import matplotlib.pyplot as plt


class Preprocessor:
    """
    A preprocessor for stored sound file information.
    """

    _duration_list: list = list()
    _loudness_list: list = list()

    _duration_max: float = 0.0
    _duration_min: float = 999999.99

    def read_csv(self, filename: str):
        """
        Reads the contents of a given CSV file
        :param filename: File name of the CSV file
        """

        with open(filename, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self._duration_list.append(float(row['endtime']))
                self._loudness_list.append(float(row['loudness']))
            self._process_duration()

    def process_loudness(self):
        """
        Normalizes the internal list to prepare the data for clustering.
        """
        # print(self._loudness_list)

        loudness_max: float = 0.0
        loudness_min: float = 999999.99

        for loudness in self._loudness_list:
            if loudness > loudness_max:
                loudness_max = loudness
            if loudness < loudness_min:
                loudness_min = loudness

        print("\nHI: %.2f, LO: %.2f" % (loudness_max, loudness_min))
        factor = 1 / (loudness_max - loudness_min)

        for index, loudness in enumerate(self._loudness_list):
            self._loudness_list[index] = round((loudness - loudness_min) * factor, 3)
        # print(self._loudness_list)

    def _process_duration(self):
        """
        Changes timestamps to durations to prepare the data for clustering.
        """
        # print(self._duration_list)
        start_time = 0.0

        for index, end_time in enumerate(self._duration_list):

            duration = round(end_time - start_time, 3)

            if duration > self._duration_max:
                self._duration_max = duration

            if duration < self._duration_min:
                self._duration_min = duration

            #if duration > 1.0:
            #    self._duration_list[index] = 1.0
            #else:
            self._duration_list[index] = duration

            start_time = end_time
        # print(self._duration_list)

    def plot(self, series: bool = False):
        """
        Plots the current state of the internal lists.
        :param series: Should the plot be displayed as a time series?
        """

        if series:
            print("Plotting scatter plot ...")
            plt.plot(self._duration_list, self._loudness_list, 'bo')
            plt.axis([self._duration_min - .1, self._duration_max + .1, -.1, 1.1])
        else:
            print("Plotting time series ...")
            x = list()
            y = list()
            start = 0.0
            for index in range(2 * len(self._duration_list)):
                if index % 2 == 0:
                    x.append(start)
                else:
                    x.append(start + self._duration_list[math.floor(index / 2)])
                    start += 0.001 + self._duration_list[math.floor(index / 2)]
                y.append(self._loudness_list[math.floor(index / 2)])

            fig = plt.figure(figsize=(25, 5))
            ax = fig.add_subplot(111)
            ax.plot(x, y, 'bo-')
            plt.axis([-.1, x[-1] + .1, -.1, 1.1])
        plt.show()

    def get_batch(self) -> list:
        """
        Returns the processed data as a list of tuples.
        :return: A list of tuples consisting of duration and loudness
        """
        return list(zip(self._duration_list, self._loudness_list))


if __name__ == "__main__":
    preprocessor = Preprocessor()
    preprocessor.read_csv('testdata.csv')
    preprocessor.plot(False)
    preprocessor.plot(True)
    preprocessor.process_loudness()
    preprocessor.plot(False)
    preprocessor.plot(True)
