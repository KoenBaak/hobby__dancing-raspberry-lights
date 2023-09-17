import os
import dotenv

from .client import Client
from .audio import AudioManager


if __name__ == "__main__":
    dotenv.load_dotenv("config.env")

    chunk_size = int(os.environ["CHUNK_SIZE"])
    dev_index = os.environ.get("DEV_INDEX", None)
    dev_index = int(dev_index) if dev_index is not None else None
    host = os.environ["HOST"]
    port = int(os.environ["PORT"])

    client = Client(host=host, port=port)
    audio = AudioManager()
    stream, rate, channels = audio.open_loopback_stream(
        chunk_size=chunk_size, dev_index=dev_index
    )

    try:
        client.run(stream, chunk_size, rate, channels)
    except ConnectionError:
        print("connection is dead, shutting down")
    finally:
        audio.shutdown()
        client.close()
