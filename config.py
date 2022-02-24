import os
from dotenv import load_dotenv

file_dir = dir_path = os.path.dirname(os.path.realpath(__file__))
env_file_path = os.path.join(file_dir, ".env")
load_dotenv(env_file_path)


class Config:
    FRAMES_PER_BUFFER = os.getenv("FRAMES_PER_BUFFER")
    FORMAT = os.getenv("FORMAT")
    CHANNELS = os.getenv("CHANNELS")
    RATE = os.getenv("RATE")
    API_KEY = os.getenv("API_KEY")
    WSS_URL = os.getenv("WSS_URL")
    SLOW_WPM_TRESHOLD = os.getenv("SLOW_WPM_TRESHOLD")
    FAST_WPM_TRESHOLD = os.getenv("FAST_WPM_TRESHOLD")

    @classmethod
    def get_fast_wpm_treshold(cls):
        return int(cls.FAST_WPM_TRESHOLD)

    @classmethod
    def get_slow_wpm_treshold(cls):
        return int(cls.SLOW_WPM_TRESHOLD)

    @classmethod
    def get_channels(cls):
        return int(cls.CHANNELS)

    @classmethod
    def get_rate(cls):
        return int(cls.RATE)

    @classmethod
    def get_frames_per_buffer(cls):
        return int(cls.FRAMES_PER_BUFFER)
