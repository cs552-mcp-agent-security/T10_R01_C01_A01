"""Build and execute ffmpeg subprocess calls based on a profile dict."""
from __future__ import annotations

import subprocess
from pathlib import Path


def build_ffmpeg_command(profile: dict, input_path: Path, output_path: Path) -> list[str]:
    """Translate a profile dict into an ffmpeg argv list."""
    cmd = ["ffmpeg", "-i", str(input_path)]

    container = profile["container"]
    if container == "gif":
        # Single-pass palette generation. See profiles.toml note about quality.
        fps = profile.get("fps", 12)
        scale = profile.get("scale", "480:-1")
        cmd += ["-vf", f"fps={fps},scale={scale}:flags=lanczos"]
    else:
        video_codec = profile["video_codec"]
        audio_codec = profile["audio_codec"]
        cmd += ["-c:v", video_codec, "-c:a", audio_codec]
        if "video_bitrate" in profile:
            cmd += ["-b:v", profile["video_bitrate"]]
        if "crf" in profile:
            cmd += ["-crf", str(profile["crf"])]
        scale = profile.get("scale")
        if scale and scale != "source":
            cmd += ["-vf", f"scale={scale}"]

    cmd.append(str(output_path))
    return cmd


def run(cmd: list[str]) -> int:
    return subprocess.call(cmd)
