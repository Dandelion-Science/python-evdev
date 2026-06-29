import os
import subprocess
import sys

import pytest


def _is_freethreaded_build() -> bool:
    import sysconfig

    return bool(sysconfig.get_config_var("Py_GIL_DISABLED"))


@pytest.mark.skipif(not _is_freethreaded_build(), reason="requires free-threaded Python build")
def test_evdev_does_not_reenable_gil():
    # Run with PYTHON_GIL unset (not 0): PYTHON_GIL=0 force-disables the GIL
    # regardless of the module, which would make this pass even for a C extension
    # that has not declared Py_MOD_GIL_NOT_USED. We want the default behavior so
    # importing a non-free-threaded extension actually re-enables the GIL and fails.
    env = {k: v for k, v in os.environ.items() if k != "PYTHON_GIL"}
    result = subprocess.run(
        [sys.executable, "-c", "import sys; import evdev; assert not sys._is_gil_enabled()"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, f"evdev re-enabled the GIL:\n{result.stderr}"
