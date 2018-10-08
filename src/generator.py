import csv
import random
from _datetime import datetime


class Generator:
    """
    A generator for simulated morse code signals.
    """

    _reference_loundness = 0.65

    _generated_endtimes_list = list()
    _generated_loudness_list = list()

    def __init__(self, noise: float, deviation_duration: float, deviation_loudness: float, wpm: int):
        """
        Configures the generator.
        :param noise: The added noise to the signal in percent
        :param deviation_duration: The variance of the duration of a signal in percent
        :param deviation_loudness: The variance of the loudness of a signal in percent
        :param wpm: Speed as defined by 'words per minute'
        """
        self._deviation_duration = deviation_duration
        self._deviation_loudness = deviation_loudness

        self._noise = noise
        self._dit_speed = self._calculate_speed_from_wpm(wpm)

    def simulate(self, message: str):
        """
        Generates a simulation based on the passed morse code message.
        :param message: A message comprised of dots, dashes and spaces
        """

        _generated_durations_list = list()

        pause_counter: int = 0
        is_still_pause: bool = True
        first_run = True
        duration = 0.0
        loudness = 0.0

        for signal in message:
            if signal == '.':
                # Dit signal
                is_still_pause = False
                duration = self._generate_duration(1)
                loudness = self._generate_loudness(self._reference_loundness)
            elif signal == '-':
                # Dah signal
                is_still_pause = False
                duration = self._generate_duration(3)
                loudness = self._generate_loudness(self._reference_loundness)
            elif signal == ' ':
                # Pause signal
                pause_counter += 1
            else:
                print("(!) ERROR (!) Invalid character within the message")

            # Add a short pause after every signal
            pause_counter += 1
            if not is_still_pause:
                if first_run:
                    first_run = False
                else:
                    pause_duration = self._generate_duration(pause_counter)
                    pause_loudness = self._generate_loudness(0)

                    # Save pause before signal
                    _generated_durations_list.append(pause_duration)
                    self._generated_loudness_list.append(pause_loudness)

                _generated_durations_list.append(duration)
                self._generated_loudness_list.append(loudness)

                # Reset
                pause_counter = 0
                is_still_pause = True

        endtime = 0.0
        for duration in _generated_durations_list:
            endtime += duration
            self._generated_endtimes_list.append(endtime)

    def _generate_duration(self, factor: int) -> float:

        min_duration = factor * self._dit_speed * (100 - self._deviation_duration) / 100.0
        max_duration = factor * self._dit_speed * (100 + self._deviation_duration) / 100.0

        return random.uniform(min_duration, max_duration)

    def _generate_loudness(self, base: float) -> float:

        min_noise = self._noise * (100 - self._deviation_loudness) / 100.0
        max_noise = self._noise * (100 + self._deviation_loudness) / 100.0

        noise = random.uniform(min_noise, max_noise) / 100.0

        min_signal = base * (100 - self._deviation_loudness) / 100.0
        max_signal = base * (100 + self._deviation_loudness) / 100.0

        signal = random.uniform(min_signal, max_signal)
        return noise + signal

    def _calculate_speed_from_wpm(self, wpm: int) -> float:
        """
        Calculates the duration of a dit signal in seconds.

        Using the word 'PARIS' comprised of 50 dit signals as reference.
        Source: http://www.kent-engineers.com/codespeed.htm

        :param wpm: 'The specified word per minute'
        :return: A duration in seconds for the shortest signal
        """
        dit_signals_per_minute: int = wpm * 50
        seconds_per_dit_signal: float = 60.0 / dit_signals_per_minute

        print(" - Calculated a speed of %.2fs s for a dit signal for a given 'words per minute' value of %d"
              % (seconds_per_dit_signal, wpm))
        return seconds_per_dit_signal

    def export(self):
        filename = 'simulation_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
        print(" - Writing generated simulation data to '%s'." % filename)

        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['endtime'] + ['loudness'])

            for endtime, loudness in zip(self._generated_endtimes_list, self._generated_loudness_list):
                writer.writerow([round(endtime, 4)] + [round(loudness, 4)])


if __name__ == "__main__":
    # A simple message in morse code. Pauses are encoded as spaces, dit is '.' and dah is '-'
    message = "- .... .. ...   .. ...   .-   ... .. -- .--. .-.. .   - . ... -   -- . ... ... .- --. .   - .... .- -  " \
              " .. ...   .-   .-.. .. - - .-.. .   -... .. -   .-.. --- -. --. . .-.   - .... .- -.   -- -.--   ..- " \
              "... ..- .- .-..   ... .... --- .-. -   . -..- .- -- .--. .-.. . ...      .-.. --- .-. . --   .. .--. " \
              "... ..- --   -.. --- .-.. --- .-.   ... .. -   .- -- . -   . -..-   ... ..- -- -- ---   .--. .-. --- " \
              "-... .- - ..- ...   .- -.. ...- . .-. ... .- .-. .. ..- --   ...- . .-.. --..--   .- -.   .--. . .-.   " \
              ".... .- .-. ..- --   -.. . - . .-. .-. ..- .. ... ... . -      .-.. ..- -.. ..- ...   . --.- ..- .. " \
              "-.. . --   .. -.   . ..- -- --..--   ... --- .-.. ..- --   ...- --- .-.. ..- .--. - .- .-. .. .-   " \
              "-.-. --- -. ... . - . - ..- .-.   .- -.   . --- ...      -. .   --- -- -. .. ..- --   -.. . -- --- " \
              "-.-. .-. .. - ..- --   ... . .-      . .-   --.- ..- ..   -.-. .-.. .. - .-   .- .-.. -... ..- -.-. .. " \
              "..- ...   ... . -. ... .. -... ..- ...   ...- .. -..-   .- -   ...- --- .-.. ..- .--. - .- .-. .. .-   " \
              "- .... . --- .--. .... .-. .- ... - ..- ...   .. ..- -.. .. -.-. .- -... .. -   .- -.. .. .--. .. ... " \
              "-.-. .. -. --.   .- -.   --.- ..- ---      .- -.   . .-. .- -   . - .. .- --   ...- .. .-. - ..- - .   " \
              "-. . -.-. --..--   -- . .-..   . .-   .--. .- ..- .-.. ---   -. --- ... - .-. ..- -.. "

    base_noise = 18.0
    deviation_duration = 10.0
    deviation_loudness = 15.0
    words_per_minute = 12

    generator = Generator(base_noise, deviation_duration, deviation_loudness, words_per_minute)
    generator.simulate(message)
    generator.export()
