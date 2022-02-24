import base64
import asyncio
import websockets
import json
from config import Config
import fluff  # noqa
from helpers import get_wpm, get_wpm_status, start_recording
from _logging import logger


logger.debug("App started")
stream = start_recording()
logger.debug("Audio recording stream initialized")


async def start_transcription():
    """Start the transcription service that asynchronously streams audio and receives the transcription."""
    logger.info(f"Connecting to AssemblyAI...")

    async with websockets.connect(
        Config.WSS_URL,
        extra_headers=(("Authorization", Config.API_KEY),),
        ping_interval=5,
        ping_timeout=20,
    ) as assemblyai_wss:

        await asyncio.sleep(0.1)
        logger.debug("Starting wss receiver...")
        session_start = await assemblyai_wss.recv()
        session_data = json.loads(session_start)
        logger.info(
            f"Successfully connected to AssebmlyAI - session_id: {session_data.get('session_id')}"
        )

        async def stream_audio():
            """Stream audio to AssemblyAI wss - https://docs.assemblyai.com/walkthroughs#realtime-streaming-transcription"""
            stop = False
            while not stop:
                try:
                    raw_data = stream.read(
                        Config.get_frames_per_buffer(),
                        exception_on_overflow=False,
                    )
                    data = base64.b64encode(raw_data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await assemblyai_wss.send(json_data)
                except (
                    Exception,
                    websockets.exceptions.ConnectionClosedError,
                ) as e:
                    logger.exception(e)
                    stop = True
                await asyncio.sleep(0.2)

        async def receive_transcription():
            """Receive and handle the transcription."""
            stop = False
            while not stop:
                try:
                    response_raw = await assemblyai_wss.recv()
                    response = json.loads(response_raw)

                    if not response.get("text"):
                        continue

                    logger.debug(response)

                    wpm = get_wpm(
                        len(response.get("words")),
                        response.get("audio_start"),
                        response.get("audio_end"),
                    )
                    wpm_status = get_wpm_status(wpm)
                    logger.info(
                        f"You are at talking at a rate of {wpm} wpm. That rate is {wpm_status}."
                    )

                    if response.get("message_type") == "FinalTranscript":
                        logger.info(f"...\n{response.get('text')} - ({wpm} WPM)\n...")
                        with open("transcription.txt", mode="a") as f:
                            f.write(f"{response.get('text')}\n")
                except (
                    Exception,
                    websockets.exceptions.ConnectionClosedError,
                ) as e:
                    logger.exception(e)
                    stop = True

        await asyncio.gather(stream_audio(), receive_transcription())


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_transcription())
    except KeyboardInterrupt:
        logger.debug("Terminated by the user.")
        logger.info(
            "\nYou can access this session's transcription in transcription.txt file.\nGood bye!"
        )
        exit()
