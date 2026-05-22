from pathlib import Path

from vidpack import profiles, runner


def test_default_profiles_loaded():
    all_p = profiles.load_all(Path("profiles.toml"))
    assert set(all_p.keys()) == {"web", "archive", "gif"}


def test_web_profile_shape():
    p = profiles.load_profile("web", Path("profiles.toml"))
    assert p["container"] == "mp4"
    assert p["video_codec"] == "libx264"
    assert p["audio_codec"] == "aac"


def test_build_command_web():
    p = profiles.load_profile("web", Path("profiles.toml"))
    cmd = runner.build_ffmpeg_command(p, Path("in.mov"), Path("out.mp4"))
    assert cmd[0] == "ffmpeg"
    assert "libx264" in cmd
    assert "aac" in cmd
    assert cmd[-1] == "out.mp4"
