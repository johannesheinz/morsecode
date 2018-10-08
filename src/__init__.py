import logging

from input import Input
from clustering import Clustering
from decoder import Decoder
from preprocessor import Preprocessor


def start():
    # Set up logger
    logger = logging.getLogger('decoder')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Set up components
    preprocessor = Preprocessor()
    clustering = Clustering(5)
    decoder = Decoder(logger)

    _input = Input()
    filename = _input.read_file('audio/testfile3.wav')
    # filename = _input.read_file('audio/testfile4.wav')

    preprocessor.read_csv(filename)
    # preprocessor.read_csv('simulation_2018-09-27_17-13-19.csv')
    preprocessor.plot()
    preprocessor.plot(True)

    preprocessor.process_loudness()
    preprocessor.plot()
    preprocessor.plot(True)

    training_batch = preprocessor.get_batch()
    labels = clustering.train(training_batch)
    mapping = clustering.get_label_mapping()
    signals = list()

    for label in labels:
        signals.append(mapping.get(label))

    for signal in signals:
        decoder.decode(signal)

    print(decoder.message)

    # clustering.train2(training_batch)


if __name__ == "__main__":
    start()
