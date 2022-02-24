import logging


# NOTE: I used the stream logger to talk to the user rather than print() so that I can have a record of that too
logger = logging.getLogger("transcription")
stream_formatter = logging.Formatter("%(message)s")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename="log.log")

stream_handler.setFormatter(stream_formatter)
file_handler.setFormatter(file_formatter)

stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
