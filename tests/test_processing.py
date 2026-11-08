import subprocess
from pathlib import Path

import pytest

from scale_lab.processing import transcode_to_opus


def test_transcode_to_opus(tmp_path: Path) -> None:
    input_path = tmp_path / "input.wav"
    output_path = tmp_path / "output.opus"

    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:sample_rate=48000:duration=2",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(input_path),
        ],
        check=True,
    )

    transcode_to_opus(input_path, output_path)

    assert output_path.is_file()
    assert output_path.stat().st_size > 0

    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_name",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == "opus"


def test_transcode_to_opus_missing_input(tmp_path: Path) -> None:
    input_path = tmp_path / "missing.wav"
    output_path = tmp_path / "output.opus"

    with pytest.raises(subprocess.CalledProcessError):
        transcode_to_opus(input_path, output_path)

    assert not output_path.exists()
