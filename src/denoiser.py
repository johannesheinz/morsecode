class Denoiser:
    """
    A tool to reduce noise in a given audio signal.
    """

    def __init__(self, level: float, smoothing: bool) -> None:
        """
        Sets the global configuration for this noise cancelling processor.
        :param level:
        :param smoothing:
        """
        self._level = level
        self._smooting = smoothing

    def process_chunk(self, chunk: bytearray) -> bytearray:
        """
        Optimizes a given chunk of sound data with the set global configuration.
        :param chunk:
        :return: The optimized version of the given sound.
        """
        print(len(chunk))
        return chunk
