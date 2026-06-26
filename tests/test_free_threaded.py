import os
import subprocess
import sys

import pytest


def _is_freethreaded_build():
    import sysconfig
    return bool(sysconfig.get_config_var("Py_GIL_DISABLED"))


@pytest.mark.skipif(not _is_freethreaded_build(), reason="requires free-threaded Python build")
def test_evdev_does_not_reenable_gil():
    result = subprocess.run(
        [sys.executable, "-c", "import sys; import evdev; assert not sys._is_gil_enabled()"],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHON_GIL": "0"},
    )
    assert result.returncode == 0, f"evdev re-enabled the GIL:\n{result.stderr}"
