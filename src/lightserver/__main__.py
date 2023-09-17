import os

import dotenv

from pilights import StripManager
from .server import Server

if __name__ == "__main__":

    dotenv.load_dotenv("config.env")

    host = os.environ["HOST"]
    port = int(os.environ["PORT"])
    pinnr = int(os.environ["PIN"])
    npixels = int(os.environ["NPIXELS"])
    color_order = os.environ.get("COLOR_ORDER", "RGB")

    server = Server(host=host, port=port)
    strip_manager = StripManager(pin_nr=pinnr,
                                 npixels=npixels,
                                 order=color_order)

    try:
        server.run(strip_manager)
    finally:
        server.shutdown()


