import csv
import sys
import wave
from _datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from scipy.fftpack import fft


# Based on the source code of 'Rattlesnake', a script for active noise cancellation.
# > Source: https://github.com/loehnertz/rattlesnake
# > Author: Jakob Löhnertz

# Also based on the source code of 'Audio-Spectrum-Analyzer-in-Python'
# > Source: https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python
# > Author: Mark Jay

class Input:

    def __init__(self):

        # stream constants
        self.CHUNK = 256
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 8000
        self.pause = False

        # Loudness area in which the signal is thought to be the same
        self.TOLERANCE = 0.48  # 0.225

        # stream object
        self.pa = pyaudio.PyAudio()

    def _read_waveaudio(self, file):
        """
        Reads in the given wave file and returns a new PyAudio stream object from it.
        :param file: The path to the file to read in
        :return (waveform, stream): (The actual audio data as a waveform, the PyAudio object for said data)
        """

        # Open the waveform from the command argument
        try:
            waveform = wave.open(file, 'rb')
        except wave.Error:
            print('The program can only process wave audio files (.wav)')
            sys.exit()
        except FileNotFoundError:
            print('The chosen file does not exist')
            sys.exit()

        print("Sample width: %d" % waveform.getsampwidth())
        print("Format: %d" % self.pa.get_format_from_width(waveform.getsampwidth()))
        print("Channels: %d" % waveform.getnchannels())
        print("Framerate: %d" % waveform.getframerate())

        # Load PyAudio and create a useable waveform object
        self.stream = self.pa.open(
            format=self.pa.get_format_from_width(waveform.getsampwidth()),
            channels=waveform.getnchannels(),
            rate=waveform.getframerate(),
            input=True,
            output=False,
            frames_per_buffer=self.CHUNK,
        )

        # self.stream = self.pa.open(
        #     format=self.FORMAT,
        #     channels=self.CHANNELS,
        #     rate=self.RATE,
        #     input=True,
        #     output=True,
        #     frames_per_buffer=self.CHUNK,
        # )

        # Return the waveform as well as the generated PyAudio stream object
        return waveform  # , stream

    def _export(self, tuples: list) -> str:
        filename = 'waveaudio_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
        print(" - Writing read audio wave data to '%s'." % filename)

        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['endtime'] + ['loudness'])

            for endtime, loudness in tuples:
                writer.writerow([round(endtime, 4)] + [round(loudness, 4)])
        return filename

    def _plot_wave(self, amplitudes):

        # Find out max value for normalization
        maxPCM = 0
        for pcmMax in np.abs(amplitudes):
            if pcmMax is not np.nan and pcmMax > maxPCM:
                maxPCM = pcmMax

        counter = 1
        previous = 0.0
        x = list()
        y = list()
        average = [0.0]

        for pcmMax in np.array(amplitudes):

            normalized = abs(pcmMax / maxPCM)

            if abs(normalized - previous) > self.TOLERANCE:

                # Signal has changed
                if previous < 0.4 and normalized > 0.6:
                    y.append(np.min(average))
                elif previous > 0.6 and normalized < 0.4:
                    y.append(np.max(average))
                else:
                    y.append(np.mean(average))
                x.append(counter)
                average.clear()

            average.append(normalized)
            previous = normalized
            counter += 1

        print("Length amplitudes: %d, Length y: %d, Max amplitude: %f" % (len(amplitudes), len(y), maxPCM))

        # absys = np.abs(amplitudes)
        # print(len(absys))
        # print("#############################################")
        # for p, absy in zip(y, absys):
        #    print('p: %f, abs: %f' % (p, absy))
        # print("#############################################")

        # Display the plotted graph
        fig = plt.figure(figsize=(25, 5))
        ax = fig.add_subplot(111)
        ax.plot(x, y, 'b')
        plt.show()

        return list(zip(x, y))

    def read_file(self, filename: str) -> list:
        """
        Reads a sound file and extracts data.
        :param filename:
        :return:
        """
        print("Opening sound file '%s' ..." % filename)

        # Read in the given file
        # (waveform, stream) = self._read_waveaudio(filename)

        waveform = self._read_waveaudio(filename)
        fmt = self.pa.get_format_from_width(waveform.getsampwidth())

        originals = list()
        fouriers = list()

        # Counting the iterations of the while-loop
        iteration = 0

        # Read a first chunk and continue to do so for as long as there is a stream to read in
        original = waveform.readframes(self.CHUNK)

        threshold = 0.0

        while original != b'':

            try:
                # Read byte array as signed 16 bit PCM data
                _bytes = np.frombuffer(original, dtype=np.int16)
                originals.extend(_bytes)

                # Read as floats
                # if len(original) % 4 == 0:
                #    format = int(len(original) / 4) * 'f'
                #    unpacked = struct.unpack(format, original)

                # try:
                #    data_int = struct.unpack(str(2 * self.CHUNK) + 'B', original)
                # except struct.error:
                #    break

                _fft = fft(_bytes)
                # Reduce FFT to relevant values (exclude edge cases)
                lower_bound: int = 10
                upper_bound: int = round(0.45 * len(_fft))
                fourier = (np.abs(_fft[0:self.CHUNK]) / (128 * self.CHUNK))[lower_bound:upper_bound]

                if len(fourier) > 0:
                    fourier_max = np.max(fourier)
                    fourier_min = np.min(fourier)

                    # Set threshold to 50%
                    if fourier_max > 2 * threshold:
                        threshold = fourier_max / 2

                    if fourier_max > threshold:  # self.THRESHOLD_FOURIER:
                        fouriers.append(fourier_max)
                    else:
                        fouriers.append(fourier_min)

                ##################################################################################

                # print(fourier)
                # print(np.abs(fourier[0:self.CHUNK]) / (128 * self.CHUNK))

                # fig = plt.figure(figsize=(7, 4))
                # ax = fig.add_subplot(111)
                # xf = np.linspace(0, self.RATE, self.CHUNK)
                # line_fft, = ax.semilogx(xf, np.random.rand(self.CHUNK), '-', lw=2)

                # line_fft.set_ydata((np.abs(fourier[0:self.CHUNK]) / (128 * self.CHUNK)))
                # plt.show()

                # print(np.max((np.abs(fourier[0:self.CHUNK]) / (128 * self.CHUNK))))

                # originals.extend(np.array(data_int, dtype='b')[::2] + 128)

                ##################################################################################

                # Read in the next chunk of data
                original = waveform.readframes(self.CHUNK)

                # Add up one to the iterations
                iteration += 1

            except (KeyboardInterrupt, SystemExit):
                break

        # Stop the stream after there is no more data to read
        self.stream.stop_stream()
        self.stream.close()

        # Plot input stream and derived max/min FFT
        _, (ax1, ax2) = plt.subplots(2, figsize=(20, 6))
        ax1.plot(originals, 'g')
        ax2.plot(fouriers, 'r')
        plt.show()

        # Terminate PyAudio as well as the program
        self.pa.terminate()

        # sys.exit()

        tuples = self._plot_wave(fouriers)

        samplewidth = waveform.getsampwidth()
        framerate = int(waveform.getframerate())

        seconds = (iteration * samplewidth * self.CHUNK) / (2 * framerate)
        print("Estimated duration (s): %f" % seconds)

        # print("LENGTHS: iterations: %d, originals: %d, fouriers: %d, tuples: %d" % (iteration, len(originals), len(fouriers), len(tuples)))

        # Transform time unit to seconds
        factor = seconds / iteration
        tuples_in_seconds = list()
        for endtime, loudness in tuples:
            tuples_in_seconds.append((factor * endtime, loudness))

        # TODO: Normalize durations to ~12 WPM

        # Return filename of the exported file
        return self._export(tuples_in_seconds)


def record_microphone(self, resolution: int) -> None:
    print(resolution)
    pass


if __name__ == "__main__":
    _input = Input()
    _input.read_file('testfile.wav')
