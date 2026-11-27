"""The deploy script must reject malformed versions before touching release state."""
import os
from pathlib import Path
import shutil
import subprocess

import pytest


SH = shutil.which("sh")
pytestmark = pytest.mark.skipif(SH is None, reason="Deployment checks need a POSIX shell")
MOCK_RELEASE_TOOLS = """
record_call() { printf '%s\\n' "$*" >> "$CALL_LOG"; return 71; }
git() { record_call git "$@"; }
docker() { record_call docker "$@"; }
curl() { record_call curl "$@"; }
sed() { record_call sed "$@"; }
. "$0"
"""


@pytest.fixture
def deploy_fixture(tmp_path):
    folder = tmp_path / "docker"
    folder.mkdir()
    script = folder / "deploy.sh"
    source = Path(__file__).resolve().parents[1] / "docker" / "deploy.sh"
    script.write_bytes(source.read_bytes())
    settings = folder / ".env"
    settings.write_text("IMAGE_TAG=v0.0.1\n", encoding="utf-8")
    calls = tmp_path / "calls.log"
    # Shell functions stop the first release operation without executing temporary files.
    env = {"PATH": os.defpath, "CALL_LOG": str(calls), "LC_ALL": "C"}
    return script, settings, calls, env


@pytest.mark.parametrize("args", [
    [], [""], ["1.2.3"], ["v1"], ["v1.2"], ["v1..3"], ["v.2.3"],
    ["v1.2."], ["v1.2.3.4"], ["v1.2.3-beta"], ["v1.2.3/extra"],
    ["v1.2.3&"], ["v1.2.3;exit"], ["v1.2.3$(printf marker)"],
    ["v1.2.3\n"], ["v1.2.3\nv4.5.6"], ["v1.2.3\r"], [" v1.2.3"],
    ["v1.2.3 "], ["v1.2.3", "extra"], ["v1.2.3v"], ["v1.2.-3"],
])
def test_invalid_release_version_has_no_side_effects(deploy_fixture, args):
    script, settings, calls, env = deploy_fixture
    result = subprocess.run(
        [SH, "-c", MOCK_RELEASE_TOOLS, str(script), *args],
        env=env, capture_output=True, text=True, timeout=5,
    )
    assert result.returncode == 2
    assert "Usage:" in result.stderr
    assert not calls.exists(), "invalid input must not invoke release tools"
    assert settings.read_text(encoding="utf-8") == "IMAGE_TAG=v0.0.1\n"


@pytest.mark.parametrize("version", ["v0.0.0", "v1.2.3", "v12.34.567", "v01.002.3"])
def test_numeric_release_version_reaches_fetch(deploy_fixture, version):
    script, settings, calls, env = deploy_fixture
    result = subprocess.run(
        [SH, "-c", MOCK_RELEASE_TOOLS, str(script), version],
        env=env, capture_output=True, text=True, timeout=5,
    )
    assert result.returncode == 71, result.stderr
    assert "fetch --quiet --tags --force origin" in calls.read_text(encoding="utf-8")
    assert settings.read_text(encoding="utf-8") == "IMAGE_TAG=v0.0.1\n"
