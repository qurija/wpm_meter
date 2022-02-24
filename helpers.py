from config import Config
from _logging import logger
import pyaudio


def get_wpm(word_count: int, start_time_ms: int, end_time_ms: int) -> int:
    """Get wpm rate using the word count in a timespan."""
    timespan_s = (end_time_ms - start_time_ms) / 1000
    return round(word_count / timespan_s * 60)


def _colorize(status: str) -> str:
    """Colorize the status words in the terminal."""
    red = "\033[1;31m"
    blue = "\033[1;34m"
    reset = "\033[0;0m"

    return f"{blue if status == 'too slow' else red}{status}{reset}"


def get_wpm_status(wpm: int):
    """Determine the status of the current wpm rate."""
    if wpm < Config.get_slow_wpm_treshold():  # TODO: add 120 to config
        return _colorize("too slow")
    elif wpm > Config.get_fast_wpm_treshold():  # TODO: add 160 to config
        return _colorize("too fast")
    else:
        return "good"


def start_recording() -> pyaudio.Stream:
    """Start recording using pyaudio."""
    p = pyaudio.PyAudio()

    device_idx = take_user_input(p)

    try:
        stream = p.open(
            format=pyaudio.paInt16,
            channels=Config.get_channels(),
            rate=Config.get_rate(),
            input=True,
            frames_per_buffer=Config.get_frames_per_buffer(),
            input_device_index=device_idx,
        )
    except OSError as e:
        logger.info("This input device is not working, try another one.")
        logger.info(str(e))
        exit()

    return stream


def take_user_input(p: pyaudio.PyAudio) -> int:
    # get available devices
    device_count = p.get_device_count()
    devices = [p.get_device_info_by_index(i) for i in range(device_count)]

    if len([device for device in devices if device.get("maxInputChannels")]) == 0:
        logger.info(
            f"No available input devices.\nTry troubleshooing your audio before trying again."
        )
        exit()

    # # only input devices are an option
    # input_devices = [device for device in devices if device.get("maxInputChannels")]

    logger.info("\nAvailable input devices:\n")
    for idx, device in enumerate(devices, start=1):
        if device.get("maxInputChannels"):
            logger.info(f"[{idx}] {device.get('name')}")

    device_idx_raw = input(
        "\nInput the number of the device you want to use for recording: "
    )
    try:
        device_idx = int(device_idx_raw) - 1
    except ValueError:
        logger.info("Invalid input, try again.")
        exit()

    try:
        devices[device_idx]
        logger.debug(
            f"User choose option {device_idx} ({devices[device_idx-1].get('name')})"
        )
    except IndexError:
        logger.debug(
            "The device you choose is not in the list of available input devices, try again."
        )
        exit()

    return device_idx
