import subprocess
from pathlib import Path


def transcode_to_opus(input_path: Path, output_path: Path) -> None:
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-nostdin",
        "-n",
        "-i",
        str(input_path),
        "-c:a",
        "libopus",
        "-b:a",
        "64k",
        "-vbr",
        "on",
        "-compression_level",
        "10",
        "-application",
        "audio",
        str(output_path),
    ]

    subprocess.run(command, check=True)
