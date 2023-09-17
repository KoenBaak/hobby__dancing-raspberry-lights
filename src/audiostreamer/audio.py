import pyaudio
import sys


class AudioManager:
    def __init__(self):
        self._p = pyaudio.PyAudio()
        self._stream = None

    def find_WASAPI_output(self):
        result = []

        for index in range(self._p.get_device_count()):
            info = self._p.get_device_info_by_index(index)
            host_api_index = info["hostApi"]
            host_api_info = self._p.get_host_api_info_by_index(host_api_index)
            if "WASAPI" in host_api_info["name"] and info["maxInputChannels"] == 0:
                result.append(info)

        return result

    def shutdown(self):
        self.close_stream()
        self._p.terminate()

    def close_stream(self):
        self._stream.stop_stream()
        self._stream.close()

    def open_loopback_stream(self, chunk_size, dev_index=None):
        if "win" in sys.platform:
            return self.open_loopback_stream_windows(
                chunk_size=chunk_size, dev_index=dev_index
            )
        else:
            if dev_index is None:
                raise RuntimeError(
                    f"Automatic loopback and device detection is only available on windows"
                )
            raise self._open_loopback_stream(chunk_size, dev_index)

    def _open_loopback_stream(self, chunk_size, dev_index):
        info = self._p.get_device_info_by_index(dev_index)
        channels = max(info["maxInputChannels"], info["maxOutputChannels"])
        rate = int(info["defaultSampleRate"])

        if channels != 2:
            raise RuntimeError(f"{channels} not supported yet")

        self._stream = self._p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk_size,
            input_device_index=dev_index,
        )

        return self._stream, rate, channels

    def open_loopback_stream_windows(self, chunk_size, dev_index=None):
        if dev_index is None:
            wasapi_output_devices = self.find_WASAPI_output()
            if len(wasapi_output_devices) == 0:
                raise RuntimeError("No WASAPI output device found")
            elif len(wasapi_output_devices) > 1:
                available = "\n".join(
                    str(d["index"]) + "  " + d["name"] for d in wasapi_output_devices
                )
                raise RuntimeError(
                    f"There are multiple WASAPI output devices found. "
                    f"You must specify which to use. "
                    f"Please set the DEV_INDEX env var.\n"
                    f"Available:\n"
                    f"{available}"
                )
            else:
                dev_index = wasapi_output_devices[0]["index"]

        info = self._p.get_device_info_by_index(dev_index)
        channels = max(info["maxInputChannels"], info["maxOutputChannels"])
        rate = int(info["defaultSampleRate"])

        if channels != 2:
            raise RuntimeError(f"{channels} not supported yet")

        self._stream = self._p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            frames_per_buffer=chunk_size,
            input_device_index=dev_index,
            as_loopback=True,
        )

        return self._stream, rate, channels
